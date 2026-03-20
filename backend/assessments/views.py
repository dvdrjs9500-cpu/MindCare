from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from assessments.models import (
    Quiz, QuizResult, UserQuizResponse, VideoAnalysis,
    EmotionFrame, AssessmentHistory, QuizQuestion
)
from assessments.serializers import (
    QuizListSerializer, QuizDetailSerializer, QuizResultSerializer,
    QuizSubmitSerializer, VideoAnalysisDetailSerializer, VideoAnalysisListSerializer,
    AssessmentHistorySerializer
)
from django.db.models import Q


class QuizViewSet(viewsets.ViewSet):
    """ViewSet for quiz management"""
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def list(self, request):
        """List all active quizzes"""
        quizzes = Quiz.objects.filter(is_active=True)
        quiz_type = request.query_params.get('type')
        if quiz_type:
            quizzes = quizzes.filter(quiz_type=quiz_type)
        serializer = QuizListSerializer(quizzes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='(?P<quiz_id>[^/.]+)')
    def retrieve(self, request, quiz_id=None):
        """Get quiz detail with all questions"""
        try:
            quiz = Quiz.objects.get(id=quiz_id, is_active=True)
            serializer = QuizDetailSerializer(quiz)
            return Response(serializer.data)
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def types(self, request):
        """Get available quiz types"""
        types = Quiz.objects.filter(is_active=True).values_list('quiz_type', flat=True).distinct()
        return Response({'quiz_types': list(types)})


class QuizResultViewSet(viewsets.ViewSet):
    """ViewSet for quiz results"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def submit_quiz(self, request):
        """Submit quiz responses"""
        serializer = QuizSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quiz = Quiz.objects.get(id=serializer.validated_data['quiz_id'])
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Calculate score
        total_score = 0
        max_score = 0
        responses_data = []
        
        for response_data in serializer.validated_data['responses']:
            question_id = int(response_data.get('question_id'))
            option_id = int(response_data.get('option_id')) if response_data.get('option_id') else None
            
            try:
                question = QuizQuestion.objects.get(id=question_id, quiz=quiz)
                max_score += question.max_score
                
                if option_id:
                    option = question.options.get(id=option_id)
                    total_score += option.score_value
                    
                    UserQuizResponse.objects.create(
                        quiz_result=None,
                        question=question,
                        selected_option=option,
                        score_received=option.score_value
                    )
                    responses_data.append({
                        'question': question.id,
                        'option': option.id,
                        'score': option.score_value
                    })
            except (QuizQuestion.DoesNotExist, Exception):
                continue
        
        # Create quiz result
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Simple diagnosis logic (should be ML-based)
        if percentage >= 80:
            diagnosis = 'SEVERE'
        elif percentage >= 60:
            diagnosis = 'MODERATE'
        elif percentage >= 40:
            diagnosis = 'MILD'
        else:
            diagnosis = 'NONE'
        
        quiz_result = QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            total_score=total_score,
            max_possible_score=max_score,
            percentage_score=percentage,
            diagnosis=diagnosis,
            confidence=0.85,
            time_taken_seconds=serializer.validated_data['time_taken_seconds'],
            device_type=serializer.validated_data['device_type']
        )
        
        # Update responses with quiz_result
        UserQuizResponse.objects.filter(quiz_result__isnull=True, question__quiz=quiz).update(quiz_result=quiz_result)
        
        # Update user's assessment history
        AssessmentHistory.objects.create(
            user=request.user,
            assessment_type='QUIZ',
            quiz_result=quiz_result,
            overall_diagnosis=diagnosis,
            overall_score=percentage,
            risk_level='HIGH' if percentage >= 60 else 'MEDIUM' if percentage >= 40 else 'LOW'
        )
        
        serializer_response = QuizResultSerializer(quiz_result)
        return Response(serializer_response.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_results(self, request):
        """Get user's quiz results"""
        results = QuizResult.objects.filter(user=request.user).order_by('-completed_at')
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))
        
        start = (page - 1) * page_size
        end = start + page_size
        
        results_page = results[start:end]
        serializer = QuizResultSerializer(results_page, many=True)
        
        return Response({
            'count': results.count(),
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='(?P<result_id>[^/.]+)', permission_classes=[permissions.IsAuthenticated])
    def retrieve_result(self, request, result_id=None):
        """Get specific quiz result"""
        try:
            result = QuizResult.objects.get(id=result_id, user=request.user)
            serializer = QuizResultSerializer(result)
            return Response(serializer.data)
        except QuizResult.DoesNotExist:
            return Response({'error': 'Result not found'}, status=status.HTTP_404_NOT_FOUND)


class VideoAnalysisViewSet(viewsets.ViewSet):
    """ViewSet for video analysis"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    @action(detail=False, methods=['get'])
    def my_analyses(self, request):
        """Get user's video analyses"""
        analyses = VideoAnalysis.objects.filter(user=request.user).order_by('-uploaded_at')
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))
        
        start = (page - 1) * page_size
        end = start + page_size
        
        analyses_page = analyses[start:end]
        serializer = VideoAnalysisListSerializer(analyses_page, many=True)
        
        return Response({
            'count': analyses.count(),
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='(?P<analysis_id>[^/.]+)')
    def retrieve_analysis(self, request, analysis_id=None):
        """Get specific video analysis"""
        try:
            analysis = VideoAnalysis.objects.get(id=analysis_id, user=request.user)
            serializer = VideoAnalysisDetailSerializer(analysis)
            return Response(serializer.data)
        except VideoAnalysis.DoesNotExist:
            return Response({'error': 'Analysis not found'}, status=status.HTTP_404_NOT_FOUND)


class AssessmentHistoryViewSet(viewsets.ViewSet):
    """ViewSet for assessment history"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_history(self, request):
        """Get user's assessment history"""
        history = AssessmentHistory.objects.filter(user=request.user).order_by('-created_at')
        
        # Filters
        assessment_type = request.query_params.get('type')
        if assessment_type:
            history = history.filter(assessment_type=assessment_type)
        
        risk_level = request.query_params.get('risk_level')
        if risk_level:
            history = history.filter(risk_level=risk_level)
        
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))
        
        start = (page - 1) * page_size
        end = start + page_size
        
        history_page = history[start:end]
        serializer = AssessmentHistorySerializer(history_page, many=True)
        
        return Response({
            'count': history.count(),
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get assessment summary/statistics"""
        assessments = AssessmentHistory.objects.filter(user=request.user)
        
        summary = {
            'total_assessments': assessments.count(),
            'quiz_assessments': assessments.filter(assessment_type='QUIZ').count(),
            'video_assessments': assessments.filter(assessment_type='VIDEO').count(),
            'high_risk': assessments.filter(risk_level='HIGH').count(),
            'medium_risk': assessments.filter(risk_level='MEDIUM').count(),
            'low_risk': assessments.filter(risk_level='LOW').count(),
        }
        
        # Get latest diagnosis
        latest = assessments.first()
        if latest:
            summary['latest_diagnosis'] = latest.overall_diagnosis
            summary['latest_date'] = latest.created_at
        
        return Response(summary)
