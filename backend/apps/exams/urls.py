from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, ExamAttemptViewSet

router = DefaultRouter()
router.register(r'', ExamViewSet, basename='exam')
router.register(r'attempts', ExamAttemptViewSet, basename='exam-attempt')

urlpatterns = [
    path('', include(router.urls)),
]
