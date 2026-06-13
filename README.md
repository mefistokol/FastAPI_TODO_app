# Todo App — Менеджер задач

Полнофункциональное веб-приложение для управления задачами и категориями. Построено на архитектуре с раздельным бэкендом и фронтендом, оркестрируемых через Docker Compose.

## Стек технологий

| Компонент | Технологии |
|-----------|------------|
| **Backend** | Python 3.12, FastAPI, SQLAlchemy 2, Pydantic v2, Uvicorn |
| **Frontend** | React 19, Axios, Nginx |
| **База данных** | PostgreSQL 16 |
| **Кэш** | Redis 8 |
| **Инфраструктура** | Docker, Docker Compose |

## Возможности

- Создание, просмотр, редактирование и удаление задач
- Отметка задач как выполненных
- Управление категориями (CRUD)
- Кэширование списков через Redis (TTL — 1 час, инвалидация при записи)
- REST API с автодокументацией (Swagger UI)

## Структура проекта

```
todo/
├── docker-compose.yml          # Оркестрация всех сервисов
├── .env                        # Переменные окружения (пароли БД и Redis)
│
├── todo-app-back/              # Backend (FastAPI)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py             # Точка входа приложения
│       ├── core/config.py      # Конфигурация (Settings)
│       ├── db/session.py       # Подключение к PostgreSQL
│       ├── cache/redis.py      # Redis-кэш
│       ├── models/             # ORM-модели (Task, Category)
│       ├── schemas/            # Pydantic-схемы
│       ├── repositories/       # Слой доступа к данным
│       ├── services/           # Бизнес-логика + кэширование
│       └── api/routers/        # Эндпоинты API
│
└── todo-app-frontend/          # Frontend (React)
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    ├── public/
    └── src/
        ├── App.js              # Главный компонент
        └── index.js            # Точка входа React
```

## Запуск

### С помощью Docker (рекомендуется)

1. Убедитесь, что установлены [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).

2. Создайте файл `.env` в корне проекта (если отсутствует):

   ```env
   POSTGRES_PASSWORD=your_postgres_password
   REDIS_PASSWORD=your_redis_password
   ```

3. Запустите все сервисы:

   ```bash
   docker compose up --build
   ```

4. Приложение будет доступно:

   | Сервис | URL |
   |--------|-----|
   | **Frontend** | http://localhost:3000 |
   | **Backend API** | http://localhost:8080 |
   | **Swagger UI** | http://localhost:8080/docs |

5. Для остановки:

   ```bash
   docker compose down
   ```

### Локальная разработка (без Docker)

Требуется запущенный PostgreSQL и Redis.

**Backend:**

```bash
cd todo-app-back
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

**Frontend:**

```bash
cd todo-app-frontend
npm install
npm start
```

Frontend dev-сервер запустится на http://localhost:3000.

## API Эндпоинты

### Задачи (`/tasks`)

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/tasks` | Список всех задач |
| `POST` | `/tasks` | Создать задачу |
| `PATCH` | `/tasks/{id}` | Обновить задачу |
| `DELETE` | `/tasks/{id}` | Удалить задачу |

### Категории (`/categories`)

| Метод | URL | Описание |
|-------|-----|----------|
| `GET` | `/categories` | Список всех категорий |
| `POST` | `/categories` | Создать категорию |
| `PATCH` | `/categories/{id}` | Обновить категорию |
| `DELETE` | `/categories/{id}` | Удалить категорию |

## Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|-----------------------|
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | — |
| `REDIS_PASSWORD` | Пароль Redis | — |
| `DATABASE_URL` | Строка подключения к БД | `postgresql+psycopg://postgres:password@localhost:5432/tododb` |
| `REDIS_URL` | Строка подключения к Redis | `redis://localhost:6379/0` |
