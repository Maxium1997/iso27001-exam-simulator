from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils import timezone
from datetime import timedelta
from .models import Exam, ExamAttempt, QuestionAnswer
from .serializers import ExamSerializer, ExamAttemptSerializer, QuestionAnswerSerializer

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.filter(status='published')
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def start(self, request, pk=None):
        """Start an exam attempt"""
        exam = self.get_object()
        
        # Check if user already has an in-progress attempt
        existing_attempt = ExamAttempt.objects.filter(
            user=request.user,
            exam=exam,
            status='in_progress'
        ).first()
        
        if existing_attempt:
            return Response(
                {'message': 'You already have an in-progress attempt for this exam'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attempt = ExamAttempt.objects.create(
            user=request.user,
            exam=exam,
            total_questions=exam.questions.count()
        )
        
        serializer = ExamAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExamAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = ExamAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExamAttempt.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def submit_answer(self, request, pk=None):
        """Submit answer to a question"""
        attempt = self.get_object()
        
        if attempt.status != 'in_progress':
            return Response(
                {'error': 'This exam attempt is not in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question_id = request.data.get('question_id')
        user_answer = request.data.get('answer')
        
        if not question_id or not user_answer:
            return Response(
                {'error': 'question_id and answer are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from apps.questions.models import Question
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
        
        is_correct = user_answer == question.correct_answer
        
        answer = QuestionAnswer.objects.create(
            attempt=attempt,
            question=question,
            user_answer=user_answer,
            is_correct=is_correct
        )
        
        if is_correct:
            attempt.correct_answers += 1
            attempt.save()
        
        serializer = QuestionAnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def submit(self, request, pk=None):
        """Submit exam attempt"""
        attempt = self.get_object()
        
        if attempt.status != 'in_progress':
            return Response(
                {'error': 'This exam attempt is not in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attempt.end_time = timezone.now()
        attempt.status = 'completed'
        attempt.score = int((attempt.correct_answers / attempt.total_questions) * 100)
        attempt.is_passed = attempt.score >= attempt.exam.passing_score
        attempt.save()
        
        serializer = ExamAttemptSerializer(attempt)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_results(self, request):
        """Get user's exam results"""
        attempts = self.get_queryset().filter(status='completed')
        serializer = self.get_serializer(attempts, many=True)
        return Response(serializer.data)
