from django.urls import path
from assessments.views import QuizViewSet, QuizResultViewSet, VideoAnalysisViewSet, AssessmentHistoryViewSet

urlpatterns = [
    # Quiz endpoints
    path('quizzes/', QuizViewSet.as_view({'get': 'list'}), name='quiz-list'),
    path('quizzes/types/', QuizViewSet.as_view({'get': 'types'}), name='quiz-types'),
    path('quizzes/<uuid:quiz_id>/', QuizViewSet.as_view({'get': 'retrieve'}), name='quiz-detail'),
    
    # Quiz Results endpoints
    path('quiz-results/submit/', QuizResultViewSet.as_view({'post': 'submit_quiz'}), name='quiz-submit'),
    path('quiz-results/my-results/', QuizResultViewSet.as_view({'get': 'my_results'}), name='quiz-my-results'),
    
    # Video Analysis endpoints
    path('videos/upload/', VideoAnalysisViewSet.as_view({'post': 'upload_video'}), name='video-upload'),
    path('videos/my-analyses/', VideoAnalysisViewSet.as_view({'get': 'my_analyses'}), name='video-my-analyses'),
    path('videos/<uuid:analysis_id>/', VideoAnalysisViewSet.as_view({'get': 'retrieve_analysis'}), name='video-detail'),
    
    # Assessment History endpoints
    path('history/my-history/', AssessmentHistoryViewSet.as_view({'get': 'my_history'}), name='assessment-my-history'),
    path('history/summary/', AssessmentHistoryViewSet.as_view({'get': 'summary'}), name='assessment-summary'),
]
