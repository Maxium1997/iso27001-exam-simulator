from django.db import models

class Question(models.Model):
    """Exam question model"""
    DIFFICULTY_CHOICES = [
        ('easy', '簡單'),
        ('medium', '中等'),
        ('hard', '困難'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('single', '單選題'),
        ('multiple', '多選題'),
        ('true_false', '是非題'),
    ]

    title = models.CharField(max_length=500)
    description = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    category = models.CharField(max_length=100)
    correct_answer = models.TextField()
    explanation = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class QuestionOption(models.Model):
    """Options for multiple choice questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    option_label = models.CharField(max_length=10)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Question Option'
        verbose_name_plural = 'Question Options'

    def __str__(self):
        return f"{self.question.title} - {self.option_label}"
