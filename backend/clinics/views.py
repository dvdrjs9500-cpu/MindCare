from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from clinics.models import Clinic, ClinicRecommendation
from clinics.serializers import (
    ClinicListSerializer, ClinicDetailSerializer,
    ClinicRecommendationSerializer, NearestClinicQuerySerializer
)
from math import radians, sin, cos, sqrt, atan2
from django.db.models import Q


class ClinicViewSet(viewsets.ViewSet):
    """ViewSet for clinic management"""
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def list(self, request):
        """List all clinics"""
        clinics = Clinic.objects.filter(is_verified=True).order_by('-average_rating')
        
        # Filters
        city = request.query_params.get('city')
        if city:
            clinics = clinics.filter(city__icontains=city)
        
        specialization = request.query_params.get('specialization')
        if specialization:
            clinics = clinics.filter(specializations__icontains=specialization)
        
        rating = request.query_params.get('min_rating')
        if rating:
            try:
                rating = float(rating)
                clinics = clinics.filter(average_rating__gte=rating)
            except ValueError:
                pass
        
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))
        
        start = (page - 1) * page_size
        end = start + page_size
        
        clinics_page = clinics[start:end]
        serializer = ClinicListSerializer(clinics_page, many=True, context={'request': request})
        
        return Response({
            'count': clinics.count(),
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='(?P<clinic_id>[^/.]+)')
    def retrieve(self, request, clinic_id=None):
        """Get clinic detail"""
        try:
            clinic = Clinic.objects.get(id=clinic_id)
            serializer = ClinicDetailSerializer(clinic)
            return Response(serializer.data)
        except Clinic.DoesNotExist:
            return Response({'error': 'Clinic not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def nearest_clinics(self, request):
        """Find nearest clinics by coordinates"""
        serializer = NearestClinicQuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_lat = serializer.validated_data['latitude']
        user_lon = serializer.validated_data['longitude']
        radius_km = serializer.validated_data.get('radius_km', 50)
        specialization = serializer.validated_data.get('specialization', '')
        
        clinics = Clinic.objects.filter(is_verified=True)
        
        if specialization:
            clinics = clinics.filter(specializations__icontains=specialization)
        
        # Calculate distance for each clinic
        def get_distance(lat2, lon2):
            R = 6371  # Earth's radius in km
            lat1, lon1 = radians(user_lat), radians(user_lon)
            lat2, lon2 = radians(lat2), radians(lon2)
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c
        
        clinics_with_distance = []
        for clinic in clinics:
            distance = get_distance(clinic.latitude, clinic.longitude)
            if distance <= radius_km:
                clinics_with_distance.append((clinic, distance))
        
        # Sort by distance
        clinics_with_distance.sort(key=lambda x: x[1])
        clinics_sorted = [clinic for clinic, _ in clinics_with_distance]
        
        serializer = ClinicListSerializer(clinics_sorted[:10], many=True)
        return Response({
            'latitude': user_lat,
            'longitude': user_lon,
            'radius_km': radius_km,
            'count': len(clinics_sorted),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def specializations(self, request):
        """Get available specializations"""
        all_specs = Clinic.objects.filter(is_verified=True).values_list('specializations', flat=True)
        specializations = set()
        for specs_str in all_specs:
            for spec in specs_str.split(','):
                specializations.add(spec.strip())
        return Response({'specializations': sorted(list(specializations))})
    
    @action(detail=False, methods=['get'])
    def cities(self, request):
        """Get all clinic cities"""
        cities = Clinic.objects.filter(is_verified=True).values_list('city', flat=True).distinct()
        return Response({'cities': sorted(list(set(cities)))})


class ClinicRecommendationViewSet(viewsets.ViewSet):
    """ViewSet for clinic recommendations"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_recommendations(self, request):
        """Get user's clinic recommendations"""
        recommendations = ClinicRecommendation.objects.filter(user=request.user).order_by('-match_percentage')
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))
        
        start = (page - 1) * page_size
        end = start + page_size
        
        recs_page = recommendations[start:end]
        serializer = ClinicRecommendationSerializer(recs_page, many=True)
        
        return Response({
            'count': recommendations.count(),
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def mark_contacted(self, request):
        """Mark recommendation as contacted"""
        recommendation_id = request.data.get('recommendation_id')
        try:
            recommendation = ClinicRecommendation.objects.get(id=recommendation_id, user=request.user)
            recommendation.is_contacted = True
            recommendation.save()
            serializer = ClinicRecommendationSerializer(recommendation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClinicRecommendation.DoesNotExist:
            return Response({'error': 'Recommendation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def mark_viewed(self, request):
        """Mark recommendation as viewed"""
        recommendation_id = request.data.get('recommendation_id')
        try:
            recommendation = ClinicRecommendation.objects.get(id=recommendation_id, user=request.user)
            recommendation.is_viewed = True
            recommendation.save()
            serializer = ClinicRecommendationSerializer(recommendation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClinicRecommendation.DoesNotExist:
            return Response({'error': 'Recommendation not found'}, status=status.HTTP_404_NOT_FOUND)
