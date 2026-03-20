"""
ML Models Package for MindCare Depression Detection
- Quiz Scorer: Naive Bayes classification for PHQ-9 assessments
- Emotion Detector: Facial analysis for video emotion detection
"""

from .quiz_scorer import QuizScorer, score_quiz, get_scorer
from .emotion_detector import EmotionDetector, detect_from_video, detect_from_frame

__all__ = [
    'QuizScorer',
    'score_quiz',
    'get_scorer',
    'EmotionDetector',
    'detect_from_video',
    'detect_from_frame',
]
