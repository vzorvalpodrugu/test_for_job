from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from Test.settings import X_API_KEY

def api_key_required(view_func):
    """Декоратор для проверки API-KEY для методов класса"""
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if not api_key or api_key != X_API_KEY:
            return Response(
                {"error": "Неверный API-Ключ"},
                status=status.HTTP_403_FORBIDDEN,
                content_type='application/json; charset=utf-8'
            )
        return view_func(self, request, *args, **kwargs)
    return wrapper