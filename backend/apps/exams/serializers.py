from rest_framework import serializers
from apps.questions.serializers import QuestionSerializer
from .models import Exam, ExamAttempt, QuestionAnswer

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'status', 'duration_minutes', 
                  'passing_score', 'questions', 'question_count', 'created_at']

    def get_question_count(self, obj):
        return obj.questions.count()


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['id', 'question', 'user_answer', 'is_correct', 'answered_at']


class ExamAttemptSerializer(serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(many=True, read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)

    class Meta:
        model = ExamAttempt
        fields = ['id', 'exam', 'exam_title', 'status', 'start_time', 'end_time', 
                  'score', 'total_questions', 'correct_answers', 'is_passed', 'answers']
