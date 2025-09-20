import pytest
from django.conf import settings
from django.contrib.auth.models import User
from core.models import Question, Answer

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        is_staff=False,
        is_superuser=False
    )

@pytest.fixture
def test_question(db):
    return Question.objects.create(text="Test question text")

@pytest.fixture
def test_answer(db, test_question):
    user, _ = User.objects.get_or_create(
        username='system_answer_bot',
        defaults={'is_staff': False, 'is_superuser': False}
    )
    return Answer.objects.create(
        question_id=test_question,
        user_id=user,
        text="Test answer text"
    )

@pytest.fixture
def valid_api_key():
    return settings.X_API_KEY