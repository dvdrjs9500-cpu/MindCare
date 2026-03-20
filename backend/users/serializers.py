from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from users.models import CustomUser, UserHealthProfile, JournalEntry, UserJournal

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'password2', 'phone']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        
        # Create health profile automatically
        UserHealthProfile.objects.create(user=user)
        
        # Create journal automatically
        UserJournal.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data


class UserHealthProfileSerializer(serializers.ModelSerializer):
    """Serializer for user health profile"""
    class Meta:
        model = UserHealthProfile
        fields = [
            'id', 'user', 'depression_type', 'severity_score', 'risk_level',
            'family_history', 'medications', 'allergies', 
            'last_assessment_date', 'total_assessments'
        ]
        read_only_fields = ['id', 'user', 'last_assessment_date', 'total_assessments']


class JournalEntrySerializer(serializers.ModelSerializer):
    """Serializer for journal entries"""
    class Meta:
        model = JournalEntry
        fields = ['id', 'user', 'title', 'content', 'mood', 'mood_score', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user profile detail"""
    health_profile = UserHealthProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'phone',
            'date_of_birth', 'gender', 'bio', 'profile_picture', 'is_diagnosed',
            'current_treatment', 'is_public_profile', 'created_at', 'updated_at',
            'health_profile'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for user list"""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
