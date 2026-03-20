from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from users.models import CustomUser, UserHealthProfile, JournalEntry
from users.serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserDetailSerializer,
    UserHealthProfileSerializer, JournalEntrySerializer, UserListSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ViewSet):
    """ViewSet for user authentication and profile management"""
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserDetailSerializer(user).data,
                'token': token.key,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Login user"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserDetailSerializer(user).data,
                'token': token.key,
                'message': 'Logged in successfully'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """Logout user"""
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        """Get user profile"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """Update user profile"""
        user = request.user
        serializer = UserDetailSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def users_list(self, request):
        """List all users (public profiles only)"""
        users = CustomUser.objects.filter(is_public_profile=True)
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)


class UserHealthProfileViewSet(viewsets.ViewSet):
    """ViewSet for user health profile"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's health profile"""
        try:
            health_profile = request.user.health_profile
            serializer = UserHealthProfileSerializer(health_profile)
            return Response(serializer.data)
        except UserHealthProfile.DoesNotExist:
            return Response({'error': 'Health profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """Update user's health profile"""
        try:
            health_profile = request.user.health_profile
            serializer = UserHealthProfileSerializer(health_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserHealthProfile.DoesNotExist:
            return Response({'error': 'Health profile not found'}, status=status.HTTP_404_NOT_FOUND)


class JournalEntryViewSet(viewsets.ViewSet):
    """ViewSet for journal entries"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def entries(self, request):
        """Get current user's journal entries"""
        entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))
        
        start = (page - 1) * page_size
        end = start + page_size
        
        entries_page = entries[start:end]
        serializer = JournalEntrySerializer(entries_page, many=True)
        
        return Response({
            'count': entries.count(),
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def add_entry(self, request):
        """Create new journal entry"""
        serializer = JournalEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'], url_path='(?P<entry_id>[^/.]+)/edit')
    def edit_entry(self, request, entry_id=None):
        """Update journal entry"""
        try:
            entry = JournalEntry.objects.get(id=entry_id, user=request.user)
            serializer = JournalEntrySerializer(entry, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JournalEntry.DoesNotExist:
            return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['delete'], url_path='(?P<entry_id>[^/.]+)/remove')
    def remove_entry(self, request, entry_id=None):
        """Delete journal entry"""
        try:
            entry = JournalEntry.objects.get(id=entry_id, user=request.user)
            entry.delete()
            return Response({'message': 'Entry deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except JournalEntry.DoesNotExist:
            return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)
