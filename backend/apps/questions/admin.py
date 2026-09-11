from django.contrib import admin
from .models import Question, QuestionOption

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question_type', 'difficulty', 'category', 'is_active')
    list_filter = ('difficulty', 'category', 'question_type', 'is_active')
    search_fields = ('title', 'description')
    inlines = [QuestionOptionInline]
    readonly_fields = ('created_at', 'updated_at')
