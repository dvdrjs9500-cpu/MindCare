from django.urls import path
from assessments.views import QuizViewSet, QuizResultViewSet, VideoAnalysisViewSet, AssessmentHistoryViewSet

urlpatterns = [
    # Quiz endpoints
    path('quizzes/', QuizViewSet.as_view({'get': 'get_quizzes'}), name='quiz-list'),
    path('quizzes/<uuid:quiz_id>/', QuizViewSet.as_view({'get': 'get_quiz'}), name='quiz-detail'),
    
    # Quiz Results endpoints
    path('quiz-results/submit/', QuizResultViewSet.as_view({'post': 'submit_quiz'}), name='quiz-submit'),
    path('quiz-results/user-results/', QuizResultViewSet.as_view({'get': 'user_results'}), name='quiz-user-results'),
    
    # Video Analysis endpoints
    path('videos/upload/', VideoAnalysisViewSet.as_view({'post': 'upload_video'}), name='video-upload'),
    path('videos/user-analyses/', VideoAnalysisViewSet.as_view({'get': 'user_analyses'}), name='video-user-analyses'),
    
    # Assessment History endpoints
    path('history/user-history/', AssessmentHistoryViewSet.as_view({'get': 'user_history'}), name='assessment-user-history'),
    path('history/summary/', AssessmentHistoryViewSet.as_view({'get': 'summary'}), name='assessment-summary'),
]
