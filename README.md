# Flask REST API

REST API для управления пользователями и задачами (работами), построенный на Flask + Flask-RESTful + SQLAlchemy. Поддерживает операции GET, POST и DELETE для двух ресурсов: пользователи (`users`) и работы (`jobs`).

## Стек

| Технология          | Назначение                        |
| ------------------- | --------------------------------- |
| Python 3.10+        | Среда выполнения                  |
| Flask               | Веб-фреймворк                     |
| Flask-RESTful       | Построение REST-ресурсов          |
| SQLAlchemy          | ORM, работа с базой данных        |
| SQLite              | База данных                       |
| sqlalchemy-serializer | Сериализация моделей в dict/JSON |

## Установка

```bash
# 1. Клонировать репозиторий
git clone <url>
cd flask-rest-api

# 2. Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить сервер
python main.py
```

Сервер запустится на `http://localhost:5000`.

## Структура проекта

```
flask-rest-api/
├── main.py                  # Точка входа, регистрация маршрутов
├── client_demo.py           # Примеры запросов к API
├── requirements.txt
├── data/
│   ├── db_session.py        # Инициализация SQLAlchemy, фабрика сессий
│   ├── __all_models.py      # Импорт всех моделей (для create_all)
│   ├── users.py             # Модель User
│   ├── jobs.py              # Модель Jobs
│   ├── users_resource.py    # REST-ресурсы /api/v2/users
│   ├── jobs_resource.py     # REST-ресурсы /api/v2/jobs
│   ├── users_parser.py      # RequestParser для создания пользователя
│   └── jobs_parser.py       # RequestParser для создания работы
└── db/
    └── blogs.db             # SQLite-файл (создаётся автоматически)
```

## Эндпоинты

### Пользователи

| Метод    | URL                        | Описание                    |
| -------- | -------------------------- | --------------------------- |
| `GET`    | `/api/v2/users`            | Список всех пользователей   |
| `GET`    | `/api/v2/users/<id>`       | Получить пользователя по ID |
| `POST`   | `/api/v2/users`            | Создать пользователя        |
| `DELETE` | `/api/v2/users/<id>`       | Удалить пользователя        |

#### Тело POST-запроса для пользователя

```json
{
  "surname": "Иванов",
  "name": "Иван",
  "age": 30,
  "position": "Инженер",
  "speciality": "Python-разработчик",
  "address": "Москва",
  "email": "ivanov@example.com",
  "hashed_password": "хэш_пароля"
}
```

### Работы (Jobs)

| Метод    | URL                     | Описание                |
| -------- | ----------------------- | ----------------------- |
| `GET`    | `/api/v2/jobs`          | Список всех работ       |
| `GET`    | `/api/v2/jobs/<id>`     | Получить работу по ID   |
| `POST`   | `/api/v2/jobs`          | Создать работу          |
| `DELETE` | `/api/v2/jobs/<id>`     | Удалить работу          |

#### Тело POST-запроса для работы

```json
{
  "team_leader": 1,
  "job": "Тестирование модуля авторизации",
  "work_size": 25,
  "collaborators": "2, 3",
  "start_date": "2024-03-20",
  "end_date": "2024-03-27",
  "is_finished": false
}
```

### Примеры ответов

**GET /api/v2/users (200):**
```json
{
  "users": [
    {
      "surname": "Иванов",
      "name": "Иван",
      "age": 30,
      "position": "Инженер",
      "speciality": "Python-разработчик",
      "address": "Москва",
      "email": "ivanov@example.com",
      "hashed_password": "хэш_пароля"
    }
  ]
}
```

**Ошибка — ресурс не найден (404):**
```json
{ "message": "Users 999 not found" }
```

**Ошибка валидации (400):**
```json
{
  "message": {
    "surname": "Missing required parameter in the JSON body or the post body or the query string"
  }
}
```

## Тесты

```bash
# Запуск всех тестов
pytest

# С подробным выводом
pytest -v

# Только тесты пользователей или работ
pytest tests/test_users.py
pytest tests/test_jobs.py
```

Тесты используют Flask Test Client и временную SQLite-базу — внешние зависимости не нужны. Перед каждым тестом таблицы очищаются автоматически.

| Файл                   | Что тестирует                              |
| ---------------------- | ------------------------------------------ |
| `tests/test_users.py`  | GET, POST, DELETE для `/api/v2/users`      |
| `tests/test_jobs.py`   | GET, POST, DELETE для `/api/v2/jobs`       |
| `tests/conftest.py`    | Инициализация тестового приложения и БД    |

## Демо-клиент

В файле `client_demo.py` содержатся готовые примеры GET, POST и DELETE запросов для обоих ресурсов. Запускать при работающем сервере:

```bash
python client_demo.py
```

## Модели данных

### User

| Поле              | Тип      | Описание             |
| ----------------- | -------- | -------------------- |
| `id`              | Integer  | Первичный ключ       |
| `surname`         | String   | Фамилия              |
| `name`            | String   | Имя                  |
| `age`             | Integer  | Возраст              |
| `position`        | String   | Должность            |
| `speciality`      | String   | Специальность        |
| `address`         | String   | Адрес                |
| `email`           | String   | Email (уникальный)   |
| `hashed_password` | String   | Хэш пароля           |
| `modified_date`   | DateTime | Дата изменения       |

### Jobs

| Поле            | Тип     | Описание                    |
| --------------- | ------- | --------------------------- |
| `id`            | Integer | Первичный ключ              |
| `team_leader`   | Integer | ID руководителя (FK users)  |
| `job`           | String  | Описание задачи             |
| `work_size`     | Integer | Объём работы (часы)         |
| `collaborators` | String  | Список соавторов            |
| `start_date`    | String  | Дата начала                 |
| `end_date`      | String  | Дата окончания              |
| `is_finished`   | Boolean | Завершена ли работа         |
