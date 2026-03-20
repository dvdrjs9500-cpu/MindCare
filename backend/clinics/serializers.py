from rest_framework import serializers
from clinics.models import Clinic, ClinicRecommendation
from math import radians, sin, cos, sqrt, atan2


class ClinicListSerializer(serializers.ModelSerializer):
    """Serializer for clinic listing"""
    distance_km = serializers.SerializerMethodField()
    
    class Meta:
        model = Clinic
        fields = [
            'id', 'name', 'city', 'state', 'phone', 'email', 'average_rating',
            'latitude', 'longitude', 'distance_km', 'is_verified'
        ]
    
    def get_distance_km(self, obj):
        # Will be calculated in view if user location provided
        request = self.context.get('request')
        if hasattr(request, 'user_lat') and hasattr(request, 'user_lon'):
            return self.calculate_distance(
                request.user_lat, request.user_lon,
                obj.latitude, obj.longitude
            )
        return None
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """Calculate distance in km between two coordinates"""
        R = 6371  # Earth's radius in km
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return round(R * c, 2)


class ClinicDetailSerializer(serializers.ModelSerializer):
    """Serializer for clinic detail"""
    class Meta:
        model = Clinic
        fields = [
            'id', 'name', 'description', 'phone', 'email', 'website',
            'address', 'city', 'state', 'postal_code', 'country',
            'latitude', 'longitude', 'specializations', 'average_rating',
            'total_reviews', 'is_verified', 'verification_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_reviews', 'verification_date']


class ClinicRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for clinic recommendations"""
    clinic_detail = ClinicDetailSerializer(source='clinic', read_only=True)
    
    class Meta:
        model = ClinicRecommendation
        fields = [
            'id', 'clinic', 'clinic_detail', 'reason', 'match_percentage',
            'distance_km', 'is_viewed', 'is_contacted', 'created_at'
        ]
        read_only_fields = ['id', 'reason', 'match_percentage', 'distance_km', 'created_at']


class NearestClinicQuerySerializer(serializers.Serializer):
    """Serializer for nearest clinic query"""
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    radius_km = serializers.IntegerField(default=50, help_text="Search radius in km")
    specialization = serializers.CharField(required=False, allow_blank=True)
