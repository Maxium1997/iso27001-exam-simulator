from django.db import models
from django.contrib.auth.models import User
from apps.questions.models import Question

class Exam(models.Model):
    """Exam model"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已發佈'),
        ('closed', '已關閉'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    duration_minutes = models.IntegerField(default=120)
    passing_score = models.IntegerField(default=70)
    total_questions = models.IntegerField()
    questions = models.ManyToManyField(Question, related_name='exams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ExamAttempt(models.Model):
    """User exam attempt record"""
    STATUS_CHOICES = [
        ('in_progress', '進行中'),
        ('completed', '已完成'),
        ('abandoned', '已放棄'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField(default=0)
    is_passed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Exam Attempt'
        verbose_name_plural = 'Exam Attempts'
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.user.username} - {self.exam.title}"


class QuestionAnswer(models.Model):
    """User's answer to a specific question"""
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Question Answer'
        verbose_name_plural = 'Question Answers'

    def __str__(self):
        return f"{self.attempt.user.username} - Q{self.question.id}"
