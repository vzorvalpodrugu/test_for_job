from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Answer
from core.serializers import QuestionSerializer, AnswerSerializer
from .utils import api_key_required

class QuestionListView(APIView):
    @api_key_required
    def post(self, request):
        """
        POST /questions/ — создать новый вопрос
        """
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_key_required
    def get(self, request):
        """
        GET /questions/ — список всех вопросов
        """
        try:
            questions = Question.objects.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
        except Question.DoesNotExist:
            return Response(
                {"error": "Вопросов не найдено!"},
                status=status.HTTP_404_NOT_FOUND
            )

class QuestionDetailView(APIView):
    @api_key_required
    def get(self, request, id):
        """
        GET /questions/{id} — получить вопрос и все ответы на него
        """
        try:
            question = Question.objects.get(id=id)
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except Question.DoesNotExist:
            return Response(
                {"error": f"Вопроса с id={id} не найдено!"},
                status=status.HTTP_404_NOT_FOUND
            )

    @api_key_required
    def delete(self, request, id):
        """
         DELETE /questions/{id} — удалить вопрос (вместе с ответами)
        """
        try:
            question = Question.objects.get(id=id)
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            return Response(
                {"error": "Вопроса с id={id} не найдено!"},
                status=status.HTTP_404_NOT_FOUND
            )

class AnswerCreateView(APIView):
    @api_key_required
    def post(self, request, id):
        """
        POST /questions/{id}/answers/ — добавить ответ к вопросу
        """
        try:
            question = Question.objects.get(id=id)
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                # Сейчас, как пользователя для ответа, будем использовать админа
                # Когда это API будет внедряться, следующую строчку нужно заменить на
                # serializer.save(question_id=question,
                #                 user_id=request.user)
                serializer.save(question_id = question ,user_id = User.objects.get(is_superuser=True))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
        except Question.DoesNotExist:
            return Response(
                {"error" : f"Вопрос с id = {id} не был найден"},
                status=status.HTTP_404_NOT_FOUND
            )

class AnswerDetailView(APIView):
    @api_key_required
    def get(self, request, answer_id):
        """
        GET /answers/{id} — получить конкретный ответ
        """
        try:
            answer = Answer.objects.get(id=answer_id)
            serializer = AnswerSerializer(answer)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Answer.DoesNotExist:
            return Response(
                {"error": f"Ответ с id = {answer_id} не был найден."},
                status=status.HTTP_404_NOT_FOUND
            )
