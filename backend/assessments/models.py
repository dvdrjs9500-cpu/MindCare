from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Quiz(models.Model):
    """Quiz templates for depression assessment"""
    QUIZ_TYPE_CHOICES = [
        ('GENERAL', 'General Depression Screen'),
        ('ANXIETY', 'Anxiety Disorder Screen'),
        ('PTSD', 'PTSD Screen'),
        ('BIPOLAR', 'Bipolar Screen'),
        ('GAD', 'Generalized Anxiety Disorder'),
        ('PHQ9', 'PHQ-9 Depression Scale'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPE_CHOICES)
    
    # Settings
    is_active = models.BooleanField(default=True)
    total_questions = models.IntegerField()
    
    # ML Model info
    model_used = models.CharField(max_length=50, default='naive_bayes')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'assessments_quiz'
        verbose_name_plural = "Quizzes"
        ordering = ['quiz_type']
    
    def __str__(self):
        return f"{self.title} (v{self.version})"


class QuizQuestion(models.Model):
    """Individual questions in a quiz"""
    QUESTION_TYPE_CHOICES = [
        ('RADIO', 'Single Choice'),
        ('CHECKBOX', 'Multiple Choice'),
        ('SCALE', 'Likert Scale'),
        ('TEXT', 'Text Response'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    
    order = models.IntegerField()
    
    # Scoring
    max_score = models.IntegerField(default=10)
    
    # Categories for grouping
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="e.g., mood, sleep, energy, etc."
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'assessments_quizquestion'
        ordering = ['quiz', 'order']
    
    def __str__(self):
        return f"Q{self.order}: {self.quiz.title}"


class QuizOption(models.Model):
    """Answer options for quiz questions"""
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    score_value = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    order = models.IntegerField()
    
    class Meta:
        db_table = 'assessments_quizoption'
        ordering = ['question', 'order']
    
    def __str__(self):
        return f"{self.question.quiz.title} - {self.option_text[:50]}"


class QuizResult(models.Model):
    """Results from a completed quiz"""
    RESULT_CHOICES = [
        ('NONE', 'No Depression Detected'),
        ('MILD', 'Mild Depression'),
        ('MODERATE', 'Moderate Depression'),
        ('SEVERE', 'Severe Depression'),
        ('ANXIETY', 'Anxiety Disorder'),
        ('PTSD', 'PTSD'),
        ('BIPOLAR', 'Bipolar Disorder'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    # Results
    total_score = models.IntegerField()
    max_possible_score = models.IntegerField()
    percentage_score = models.FloatField()
    
    # Classification
    diagnosis = models.CharField(max_length=50, choices=RESULT_CHOICES)
    confidence = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Model confidence score (0-1)"
    )
    
    # Category scores (for detailed breakdown)
    category_scores = models.JSONField(default=dict, blank=True)
    
    # Recommendations
    recommendations = models.TextField(blank=True, null=True)
    
    # Duration & device info
    time_taken_seconds = models.IntegerField()
    device_type = models.CharField(max_length=20, choices=[('WEB', 'Web'), ('MOBILE', 'Mobile')])
    
    # Timestamps
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'assessments_quizresult'
        ordering = ['-completed_at']
        indexes = [
            models.Index(fields=['user', '-completed_at']),
            models.Index(fields=['quiz', '-completed_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.diagnosis})"


class UserQuizResponse(models.Model):
    """Stores individual user responses to quiz questions"""
    quiz_result = models.ForeignKey(QuizResult, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuizOption, on_delete=models.CASCADE, null=True, blank=True)
    text_response = models.TextField(blank=True, null=True)
    score_received = models.IntegerField()
    
    class Meta:
        db_table = 'assessments_userquizresponse'
    
    def __str__(self):
        return f"{self.quiz_result.user.username} - Q{self.question.order}"


class VideoAnalysis(models.Model):
    """Video-based depression detection results"""
    EMOTION_CHOICES = [
        ('HAPPY', 'Happy'),
        ('SAD', 'Sad'),
        ('ANGRY', 'Angry'),
        ('FEAR', 'Fear'),
        ('SURPRISE', 'Surprise'),
        ('NEUTRAL', 'Neutral'),
        ('DISGUST', 'Disgust'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_analyses')
    
    # Video file
    video_file = models.FileField(upload_to='videos/%Y/%m/%d/')
    video_duration = models.IntegerField(help_text="Duration in seconds")
    
    # Analysis results
    overall_emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES)
    emotion_confidence = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # Emotion timeline (frame-by-frame analysis)
    emotion_timeline = models.JSONField(
        default=dict,
        help_text="Dictionary with timestamp and emotion for each frame"
    )
    
    # Depression indicators
    depression_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Calculated depression risk score"
    )
    depression_classification = models.CharField(
        max_length=50,
        choices=[
            ('LOW', 'Low Risk'),
            ('MEDIUM', 'Medium Risk'),
            ('HIGH', 'High Risk'),
        ]
    )
    
    # Face detection metrics
    face_count = models.IntegerField(default=1)
    frames_detected = models.IntegerField()
    total_frames = models.IntegerField()
    detection_confidence = models.FloatField(default=0.0)
    
    # Micro-expressions and behavioral indicators
    eye_contact_percentage = models.FloatField(default=0.0)
    smile_count = models.IntegerField(default=0)
    blink_rate = models.FloatField(default=0.0)  # blinks per minute
    speaking_rate = models.FloatField(default=0.0)  # estimated from video
    
    # Recommendations
    recommendations = models.TextField(blank=True, null=True)
    
    # Processing metadata
    model_version = models.CharField(max_length=50, default='v1.0')
    processing_time = models.FloatField(help_text="Processing time in seconds")
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analyzed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'assessments_videoanalysis'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user', '-uploaded_at']),
            models.Index(fields=['depression_classification']),
        ]
    
    def __str__(self):
        return f"Video Analysis - {self.user.username} ({self.depression_classification})"


class EmotionFrame(models.Model):
    """Frame-by-frame emotion detection data"""
    video_analysis = models.ForeignKey(VideoAnalysis, on_delete=models.CASCADE, related_name='frames')
    
    frame_number = models.IntegerField()
    timestamp = models.FloatField(help_text="Time in video (seconds)")
    
    # Emotions with confidence scores
    emotion = models.CharField(max_length=20, choices=VideoAnalysis.EMOTION_CHOICES)
    confidence = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # All emotion probabilities
    emotion_probabilities = models.JSONField(default=dict)
    
    # Facial landmarks (optional)
    facial_landmarks = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'assessments_emotionframe'
        ordering = ['video_analysis', 'frame_number']
    
    def __str__(self):
        return f"{self.video_analysis.user.username} - Frame {self.frame_number}"


class AssessmentHistory(models.Model):
    """Track all assessments (quiz + video) in one place"""
    ASSESSMENT_TYPE_CHOICES = [
        ('QUIZ', 'Quiz Assessment'),
        ('VIDEO', 'Video Assessment'),
        ('COMBINED', 'Combined Assessment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_history')
    
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE_CHOICES)
    
    # Links to actual results
    quiz_result = models.ForeignKey(QuizResult, on_delete=models.SET_NULL, null=True, blank=True)
    video_analysis = models.ForeignKey(VideoAnalysis, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Combined result
    overall_diagnosis = models.CharField(max_length=50)
    overall_score = models.FloatField()
    
    # Trend analysis
    risk_level = models.CharField(
        max_length=20,
        choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'assessments_history'
        ordering = ['-created_at']
        verbose_name_plural = "Assessment Histories"
    
    def __str__(self):
        return f"{self.user.username} - {self.assessment_type} ({self.created_at.date()})"
