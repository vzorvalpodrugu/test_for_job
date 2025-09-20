from django.urls import path
from .views import (
    QuestionListView,
    QuestionDetailView,
    AnswerCreateView,
    AnswerDetailView
)

urlpatterns = [
    path('questions', QuestionListView.as_view(), name='question-list'),
    path('questions/<int:id>', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:id>/answers', AnswerCreateView.as_view(), name='answer-create'),
    path('answers/<int:answer_id>', AnswerDetailView.as_view(), name='answer-detail'),
]