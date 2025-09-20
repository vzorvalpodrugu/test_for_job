Q&A API Project
Простое REST API для системы вопросов и ответов, построенное на Django и Django REST Framework.

Основные возможности
- Создание и управление вопросами

- Добавление ответов к вопросам

- API Key аутентификация

- Полностью контейнеризовано с Docker

- Полное покрытие тестами

- Логирование всех операций

API Endpoints
БЕЗ СЛЕШЕЙ В КОНЦЕ - СМОТРЕТЬ ВНИМАТЕЛЬНО
Вопросы

POST /api/questions - Создать новый вопрос

GET /api/questions - Получить список всех вопросов

GET /api/questions/{id} - Получить вопрос и все ответы на него

DELETE /api/questions/{id} - Удалить вопрос (с ответами)

Ответы
POST /api/questions/{id}/answers - Добавить ответ к вопросу

GET /api/answers/{id} - Получить конкретный ответ

DELETE /api/answers/{id} - Удалить ответ

🛠 Технологии
Backend: Django 5.2.6 + Django REST Framework

Database: PostgreSQL 15

Containerization: Docker + Docker Compose

Testing: pytest + pytest-django

Authentication: API Key

📦 Установка и запуск
1. Клонирование репозитория
git clone <your-repo-url>
cd test_for_job

2. Запуск основного приложения
# Сборка и запуск контейнеров
docker-compose up --build

# Или в фоновом режиме
docker-compose up -d --build

3. Запуск тестов
# Запуск тестов в отдельном окружении
docker-compose -f docker-compose.test.yml up --build

4. Остановка приложения
# Остановка основного приложения
docker-compose down

# Остановка тестового окружения  
docker-compose -f docker-compose.test.yml down

🔐 Настройка API Key
API использует ключ аутентификации. Для работы с API необходимо:

      Создать файл .env в корне проекта:
      X-API-KEY=your-super-secret-api-key-123
      admin_password=your-admin-password
      DATABASE_URL=database_url

      Передавать ключ в заголовках запросов:
      X-API-Key: your-super-secret-api-key-123

📝 Примеры использования API
Создание вопроса
curl -X POST http://localhost:8000/api/questions/ \
  -H "X-API-Key: your-super-secret-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{"text": "Как работает Docker?"}'

Получение списка вопросов
curl -X GET http://localhost:8000/api/questions/ \
  -H "X-API-Key: your-super-secret-api-key-123"

Я же все запросы делал через Postman по адресу http://127.0.0.1:8000/api/, но можно и http://localhost:8000/api/
Обратите внимание, что тело запроса нужно указывать в Body в Json формате, если речь идёт о POST запросе

🧪 Тестирование
Проект включает полный набор тестов:

- Тесты создания и получения вопросов

- Тесты управления ответами

- Тесты аутентификации по API Key

- Тесты обработки ошибок

Запуск тестов создает изолированное окружение с тестовой базой данных.

📊 Логирование
Приложение настроено с подробным логированием:

Логи записываются в logs/django.log

Консольный вывод для разработки

Логирование всех API запросов и ошибок

🔧 Настройка окружения
Основные переменные окружения (через .env или docker-compose):

X-API-KEY - секретный ключ API

POSTGRES_* - настройки PostgreSQL

ADMIN_PASSWORD - пароль администатора

И наконец, если понадобится запустить проект дважды, а старую БД снести, то воспользуйтесь
    docker-compose down -v
А затем
    docker-compose up --build
Чтобы собрать всё снова.

