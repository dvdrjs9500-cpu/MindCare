from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Clinic(models.Model):
    """Psychiatric clinics and hospitals"""
    SPECIALIZATION_CHOICES = [
        ('GENERAL', 'General Psychiatry'),
        ('DEPRESSION', 'Depression Specialist'),
        ('ANXIETY', 'Anxiety Disorder'),
        ('PTSD', 'PTSD Specialist'),
        ('BIPOLAR', 'Bipolar Disorder'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    
    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    
    # Coordinates for mapping
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    specializations = models.CharField(max_length=200)
    average_rating = models.FloatField(default=5.0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clinics_clinic'
        ordering = ['-average_rating', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.city}"


class ClinicRecommendation(models.Model):
    """AI-generated clinic recommendations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinic_recommendations')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    
    reason = models.TextField()
    match_percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    distance_km = models.FloatField()
    
    is_viewed = models.BooleanField(default=False)
    is_contacted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'clinics_recommendation'
        ordering = ['-match_percentage', 'distance_km']
    
    def __str__(self):
        return f"Recommendation: {self.clinic.name} for {self.user.username}"
