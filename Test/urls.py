from django.contrib import admin
from django.urls import path
from core.views import (
    QuestionListView,
    QuestionDetailView,
    AnswerCreateView,
    AnswerDetailView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/questions', QuestionListView.as_view(), name='questions'),
    path('api/questions/<int:id>', QuestionDetailView.as_view(), name='question'),
    path('api/questions/<int:id>/answers', AnswerCreateView.as_view(), name='answers'),
    path('api/answers/<int:answer_id>', AnswerDetailView.as_view(), name='detail_answer'),
]
