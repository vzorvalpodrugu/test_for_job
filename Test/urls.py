from django.contrib import admin
from django.urls import path
from core.views import QuestionViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/questions', QuestionViewSet.as_view(), name='questions_create'),
]
