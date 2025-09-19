from django.contrib import admin
from django.urls import path
from core.views import (
    QuestionListView,
    QuestionDetailView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/questions', QuestionListView.as_view(), name='questions'),
    path('api/questions/<int:id>', QuestionDetailView.as_view(), name='question'),
]
