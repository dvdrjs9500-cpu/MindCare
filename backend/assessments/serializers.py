from rest_framework import serializers
from assessments.models import (
    Quiz, QuizQuestion, QuizOption, QuizResult, UserQuizResponse,
    VideoAnalysis, EmotionFrame, AssessmentHistory
)


class QuizOptionSerializer(serializers.ModelSerializer):
    """Serializer for quiz options"""
    class Meta:
        model = QuizOption
        fields = ['id', 'option_text', 'score_value', 'order']


class QuizQuestionSerializer(serializers.ModelSerializer):
    """Serializer for quiz questions with options"""
    options = QuizOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question_text', 'question_type', 'order', 'category', 'max_score', 'options']


class QuizListSerializer(serializers.ModelSerializer):
    """Serializer for quiz listing"""
    total_questions = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'quiz_type', 'total_questions', 'version']
    
    def get_total_questions(self, obj):
        return obj.questions.count()


class QuizDetailSerializer(serializers.ModelSerializer):
    """Serializer for quiz detail with all questions"""
    questions = QuizQuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'quiz_type', 'is_active', 'questions', 'version']


class UserQuizResponseSerializer(serializers.ModelSerializer):
    """Serializer for user quiz responses"""
    class Meta:
        model = UserQuizResponse
        fields = ['id', 'question', 'selected_option', 'text_response', 'score_received']


class QuizResultSerializer(serializers.ModelSerializer):
    """Serializer for quiz results"""
    responses = UserQuizResponseSerializer(many=True, read_only=True)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    
    class Meta:
        model = QuizResult
        fields = [
            'id', 'quiz', 'quiz_title', 'total_score', 'max_possible_score',
            'percentage_score', 'diagnosis', 'confidence', 'recommendations',
            'time_taken_seconds', 'device_type', 'completed_at', 'responses'
        ]
        read_only_fields = ['id', 'total_score', 'percentage_score', 'diagnosis', 'confidence', 'completed_at']


class QuizSubmitSerializer(serializers.Serializer):
    """Serializer for submitting quiz"""
    quiz_id = serializers.IntegerField()
    responses = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    time_taken_seconds = serializers.IntegerField()
    device_type = serializers.ChoiceField(choices=['WEB', 'MOBILE'])


class EmotionFrameSerializer(serializers.ModelSerializer):
    """Serializer for emotion frames"""
    class Meta:
        model = EmotionFrame
        fields = ['id', 'frame_number', 'timestamp', 'emotion', 'confidence', 'emotion_probabilities']


class VideoAnalysisListSerializer(serializers.ModelSerializer):
    """Serializer for video analysis listing"""
    class Meta:
        model = VideoAnalysis
        fields = [
            'id', 'overall_emotion', 'depression_score', 'depression_classification',
            'uploaded_at', 'analyzed_at'
        ]


class VideoAnalysisDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed video analysis"""
    frames = EmotionFrameSerializer(many=True, read_only=True)
    
    class Meta:
        model = VideoAnalysis
        fields = [
            'id', 'video_file', 'video_duration', 'overall_emotion', 'emotion_confidence',
            'emotion_timeline', 'depression_score', 'depression_classification',
            'face_count', 'frames_detected', 'total_frames', 'detection_confidence',
            'eye_contact_percentage', 'smile_count', 'blink_rate', 'speaking_rate',
            'recommendations', 'model_version', 'processing_time', 'uploaded_at', 'analyzed_at',
            'frames'
        ]
        read_only_fields = ['id', 'depression_score', 'depression_classification', 'analyzed_at']


class AssessmentHistorySerializer(serializers.ModelSerializer):
    """Serializer for assessment history"""
    quiz_result = QuizResultSerializer(read_only=True, allow_null=True)
    video_analysis = VideoAnalysisListSerializer(read_only=True, allow_null=True)
    
    class Meta:
        model = AssessmentHistory
        fields = [
            'id', 'assessment_type', 'overall_diagnosis', 'overall_score', 'risk_level',
            'created_at', 'quiz_result', 'video_analysis'
        ]
        read_only_fields = ['id', 'created_at']
