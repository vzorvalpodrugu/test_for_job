FROM python:3.13-slim

WORKDIR /app

# Установка netcat и зависимостей
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# Установка pytest для тестов
RUN pip install pytest pytest-django pytest-factoryboy

COPY . .
EXPOSE 8000

# Команда по умолчанию (для обычного запуска)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]