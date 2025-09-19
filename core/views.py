from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question
from core.serializers import QuestionSerializer
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