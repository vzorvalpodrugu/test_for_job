from rest_framework import status
from rest_framework.response import Response
import json
from Test.settings import X_API_KEY

def check_api_key(api_key):
    """Проверка валидности API-KEY"""
    if api_key == X_API_KEY:
        return api_key

def api_key_required(view_func):
    """Декоратор для проверки API-KEY"""
    def wrapper(request):
        api_key = request.headers.get('X-API-KEY')
        if not api_key or not check_api_key(api_key):
            return Response(
                {"error" : "Неверный API-Ключ"},
                status = status.HTTP_403_FORBIDDEN
            )
        return view_func(request)
    return wrapper