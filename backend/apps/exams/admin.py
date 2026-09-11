from django.contrib import admin
from .models import Exam, ExamAttempt, QuestionAnswer

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'duration_minutes', 'passing_score', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('questions',)

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'status', 'score', 'is_passed', 'start_time')
    list_filter = ('status', 'is_passed', 'start_time')
    search_fields = ('user__username', 'exam__title')
    readonly_fields = ('start_time', 'end_time', 'score', 'correct_answers')
