from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    """Extended User model with profile and health information"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Health information
    is_diagnosed = models.BooleanField(default=False)
    current_treatment = models.TextField(blank=True, null=True)
    
    # Privacy settings
    is_public_profile = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_customuser'
        verbose_name_plural = "Custom Users"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


class UserHealthProfile(models.Model):
    """Stores user's health metrics and history"""
    DEPRESSION_TYPE_CHOICES = [
        ('NONE', 'None'),
        ('MILD', 'Mild Depression'),
        ('MODERATE', 'Moderate Depression'),
        ('SEVERE', 'Severe Depression'),
        ('ANXIETY', 'Anxiety Disorder'),
        ('PTSD', 'PTSD'),
        ('BIPOLAR', 'Bipolar Disorder'),
        ('OTHER', 'Other'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='health_profile')
    
    # Depression tracking
    depression_type = models.CharField(
        max_length=50, 
        choices=DEPRESSION_TYPE_CHOICES, 
        default='NONE'
    )
    severity_score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Mental health history
    family_history = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    
    # Assessment frequencies
    last_assessment_date = models.DateTimeField(null=True, blank=True)
    total_assessments = models.IntegerField(default=0)
    
    # Risk level (ML calculated)
    risk_level = models.CharField(
        max_length=10,
        choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')],
        default='LOW'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_healthprofile'
        verbose_name_plural = "Health Profiles"
    
    def __str__(self):
        return f"Health Profile for {self.user.username}"


class UserJournal(models.Model):
    """Personal wellness journal for users"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='journal')
    entries = models.ManyToManyField('JournalEntry', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_journal'
    
    def __str__(self):
        return f"Journal for {self.user.username}"


class JournalEntry(models.Model):
    """Individual journal entries"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='journal_entries')
    title = models.CharField(max_length=200)
    content = models.TextField()
    mood = models.CharField(
        max_length=20,
        choices=[
            ('HAPPY', 'Happy'),
            ('SAD', 'Sad'),
            ('ANXIOUS', 'Anxious'),
            ('CALM', 'Calm'),
            ('ANGRY', 'Angry'),
            ('NEUTRAL', 'Neutral'),
        ],
        default='NEUTRAL'
    )
    mood_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_journalentry'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
