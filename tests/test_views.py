import pytest
from django.urls import reverse
from rest_framework import status
from core.models import Question, Answer

pytestmark = pytest.mark.django_db


class TestQuestionListView:
    def test_create_question_success(self, api_client, valid_api_key):
        """Тест успешного создания вопроса"""
        url = reverse('question-list')  # БЕЗ core:
        data = {'text': 'New test question'}

        response = api_client.post(
            url,
            data,
            format='json',
            HTTP_X_API_KEY=valid_api_key
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Question.objects.count() == 1
        assert response.data['text'] == 'New test question'

    def test_create_question_invalid_data(self, api_client, valid_api_key):
        """Тест создания вопроса с невалидными данными"""
        url = reverse('question-list')  # БЕЗ core:
        data = {'text': ''}

        response = api_client.post(
            url,
            data,
            format='json',
            HTTP_X_API_KEY=valid_api_key
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'text' in response.data

    def test_get_questions_empty(self, api_client, valid_api_key):
        """Тест получения пустого списка вопросов"""
        url = reverse('question-list')  # БЕЗ core:

        response = api_client.get(url, HTTP_X_API_KEY=valid_api_key)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_questions_with_data(self, api_client, valid_api_key,
                                     test_question):
        """Тест получения списка вопросов с данными"""
        url = reverse('question-list')  # БЕЗ core:

        response = api_client.get(url, HTTP_X_API_KEY=valid_api_key)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['text'] == test_question.text


class TestQuestionDetailView:
    def test_get_question_success(self, api_client, valid_api_key,
                                  test_question):
        """Тест успешного получения вопроса"""
        url = reverse('question-detail',
                      kwargs={'id': test_question.id})  # БЕЗ core:

        response = api_client.get(url, HTTP_X_API_KEY=valid_api_key)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['question']['text'] == test_question.text
        assert response.data['answers'] == []

    def test_get_nonexistent_question(self, api_client, valid_api_key):
        """Тест получения несуществующего вопроса"""
        url = reverse('question-detail', kwargs={'id': 999})  # БЕЗ core:

        response = api_client.get(url, HTTP_X_API_KEY=valid_api_key)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_question_success(self, api_client, valid_api_key,
                                     test_question):
        """Тест успешного удаления вопроса"""
        url = reverse('question-detail',
                      kwargs={'id': test_question.id})  # БЕЗ core:

        response = api_client.delete(url, HTTP_X_API_KEY=valid_api_key)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Question.objects.count() == 0


class TestAnswerCreateView:
    def test_create_answer_success(self, api_client, valid_api_key,
                                   test_question):
        """Тест успешного создания ответа"""
        url = reverse('answer-create',
                      kwargs={'id': test_question.id})  # БЕЗ core:
        data = {'text': 'New test answer'}

        response = api_client.post(
            url,
            data,
            format='json',
            HTTP_X_API_KEY=valid_api_key
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Answer.objects.count() == 1
        assert response.data['text'] == 'New test answer'

    def test_create_answer_nonexistent_question(self, api_client,
                                                valid_api_key):
        """Тест создания ответа для несуществующего вопроса"""
        url = reverse('answer-create', kwargs={'id': 999})  # БЕЗ core:
        data = {'text': 'New test answer'}

        response = api_client.post(
            url,
            data,
            format='json',
            HTTP_X_API_KEY=valid_api_key
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestAnswerDetailView:
    def test_get_answer_success(self, api_client, valid_api_key, test_answer):
        """Тест успешного получения ответа"""
        url = reverse('answer-detail',
                      kwargs={'answer_id': test_answer.id})  # БЕЗ core:

        response = api_client.get(url, HTTP_X_API_KEY=valid_api_key)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == test_answer.text

    def test_delete_answer_success(self, api_client, valid_api_key,
                                   test_answer):
        """Тест успешного удаления ответа"""
        url = reverse('answer-detail',
                      kwargs={'answer_id': test_answer.id})  # БЕЗ core:

        response = api_client.delete(url, HTTP_X_API_KEY=valid_api_key)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Answer.objects.count() == 0


class TestApiKeyAuthentication:
    def test_missing_api_key(self, api_client):
        """Тест запроса без API ключа"""
        url = reverse('question-list')  # БЕЗ core:

        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_invalid_api_key(self, api_client):
        """Тест запроса с неверным API ключом"""
        url = reverse('question-list')  # БЕЗ core:

        response = api_client.get(url, HTTP_X_API_KEY='invalid-key')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_valid_api_key(self, api_client, valid_api_key, test_question):
        """Тест запроса с верным API ключом"""
        url = reverse('question-list')  # БЕЗ core:

        response = api_client.get(url, HTTP_X_API_KEY=valid_api_key)

        assert response.status_code == status.HTTP_200_OK