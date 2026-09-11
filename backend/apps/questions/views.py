from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Question, QuestionOption
from .serializers import QuestionSerializer, QuestionDetailSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_active=True)
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty', 'category', 'question_type']
    search_fields = ['title', 'description']
    ordering_fields = ['difficulty', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuestionDetailSerializer
        return QuestionSerializer

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get questions grouped by category"""
        category = request.query_params.get('category')
        if category:
            questions = Question.objects.filter(category=category, is_active=True)
            serializer = self.get_serializer(questions, many=True)
            return Response(serializer.data)
        return Response({'error': 'category parameter required'}, status=400)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all available question categories"""
        categories = Question.objects.filter(is_active=True).values_list('category', flat=True).distinct()
        return Response({'categories': list(categories)})
