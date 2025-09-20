import logging
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Answer
from core.serializers import QuestionSerializer, AnswerSerializer
from .utils import api_key_required

logger = logging.getLogger(__name__)


class QuestionListView(APIView):
    @api_key_required
    def post(self, request):
        """
        POST /questions/ — создать новый вопрос
        """
        logger.info(
            f"POST /questions/ - создание вопроса. Данные: {request.data}")

        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            question = serializer.save()
            logger.info(f"Вопрос создан успешно. ID: {question.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"Ошибка валидации вопроса: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_key_required
    def get(self, request):
        """
        GET /questions/ — список всех вопросов
        """
        logger.info("GET /questions/ - получение списка вопросов")

        try:
            questions = Question.objects.all()
            serializer = QuestionSerializer(questions, many=True)
            logger.info(f"Найдено {len(questions)} вопросов")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Ошибка при получении вопросов: {str(e)}")
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
        logger.info(f"GET /questions/{id} - получение вопроса с ответами")

        try:
            question = Question.objects.get(id=id)
            answers = Answer.objects.filter(question_id=question.id)

            question_serializer = QuestionSerializer(question)
            answer_serializer = AnswerSerializer(answers, many=True)

            logger.info(f"Вопрос {id} найден. Ответов: {answers.count()}")
            return Response(
                {
                    "question": question_serializer.data,
                    "answers": answer_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Question.DoesNotExist:
            logger.warning(f"Вопрос с id={id} не найден")
            return Response(
                {"error": f"Вопрос id={id} не найден!"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при получении вопроса {id}: {str(e)}")
            return Response(
                {"error": "Произошла ошибка при получении вопроса"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_key_required
    def delete(self, request, id):
        """
        DELETE /questions/{id} — удалить вопрос (вместе с ответами)
        """
        logger.info(f"DELETE /questions/{id} - удаление вопроса")

        try:
            question = Question.objects.get(id=id)
            answers_count = Answer.objects.filter(question_id=id).count()
            question.delete()

            logger.info(
                f"Вопрос {id} удален. Удалено ответов: {answers_count}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            logger.warning(f"Попытка удаления несуществующего вопроса id={id}")
            return Response(
                {"error": f"Вопроса с id={id} не найдено!"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при удалении вопроса {id}: {str(e)}")
            return Response(
                {"error": "Произошла ошибка при удалении вопроса"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AnswerCreateView(APIView):
    @api_key_required
    def post(self, request, id):
        """
        POST /questions/{id}/answers/ — добавить ответ к вопросу
        """
        logger.info(
            f"POST /questions/{id}/answers/ - создание ответа. Данные: {request.data}")

        try:
            question = Question.objects.get(id=id)
            serializer = AnswerSerializer(data=request.data)

            if serializer.is_valid():
                # Получаем системного пользователя
                user, created = User.objects.get_or_create(
                    username='system_answer_bot',
                    defaults={
                        'is_staff': False,
                        'is_superuser': False,
                        'is_active': True
                    }
                )

                answer = serializer.save(question_id=question, user_id=user)
                logger.info(
                    f"Ответ создан успешно. ID ответа: {answer.id}, вопрос: {id}")
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                logger.warning(f"Ошибка валидации ответа: {serializer.errors}")
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Question.DoesNotExist:
            logger.warning(
                f"Попытка создания ответа для несуществующего вопроса id={id}")
            return Response(
                {"error": f"Вопрос с id={id} не был найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                f"Ошибка при создании ответа для вопроса {id}: {str(e)}")
            return Response(
                {"error": "Произошла ошибка при создании ответа"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AnswerDetailView(APIView):
    @api_key_required
    def get(self, request, answer_id):
        """
        GET /answers/{id} — получить конкретный ответ
        """
        logger.info(f"GET /answers/{answer_id} - получение ответа")

        try:
            answer = Answer.objects.get(id=answer_id)
            serializer = AnswerSerializer(answer)
            logger.info(f"Ответ {answer_id} найден")
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Answer.DoesNotExist:
            logger.warning(f"Ответ с id={answer_id} не найден")
            return Response(
                {"error": f"Ответ с id={answer_id} не был найден."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при получении ответа {answer_id}: {str(e)}")
            return Response(
                {"error": "Произошла ошибка при получении ответа"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_key_required
    def delete(self, request, answer_id):
        """
        DELETE /answers/{id} — удалить ответ
        """
        logger.info(f"DELETE /answers/{answer_id} - удаление ответа")

        try:
            answer = Answer.objects.get(id=answer_id)
            answer.delete()
            logger.info(f"Ответ {answer_id} удален успешно")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Answer.DoesNotExist:
            logger.warning(
                f"Попытка удаления несуществующего ответа id={answer_id}")
            return Response(
                {"error": f"Ответ с id={answer_id} не был найден."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при удалении ответа {answer_id}: {str(e)}")
            return Response(
                {"error": "Произошла ошибка при удалении ответа"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )