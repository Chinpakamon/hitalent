# Chat API Service

API для работы с чатами и сообщениями.  
Реализовано на **FastAPI**, **SQLAlchemy** и **PostgreSQL**, полностью контейнеризовано с помощью Docker и docker-compose.

---

## Оглавление

- [Описание проекта](#описание-проекта)
- [Модели данных](#модели-данных)
- [API](#api)
  - [Создание чата](#post-chats)
  - [Отправка сообщения](#post-chatsidmessages)
  - [Получение чата с последними сообщениями](#get-chatsid)
  - [Удаление чата](#delete-chatsid)
- [Валидация и ограничения](#валидация-и-ограничения)
- [Запуск проекта](#запуск-проекта)
- [Миграции базы данных](#миграции-базы-данных)
- [Тестирование](#тестирование)
- [Линтеры и форматирование кода](#линтеры-и-форматирование-кода)
- [Docker и docker-compose](#docker-и-docker-compose)

---

## Описание проекта

Сервис предоставляет API для:

- Создания чатов
- Отправки сообщений в чаты
- Получения чата с последними N сообщениями
- Удаления чатов и связанных с ними сообщений

Сервис использует **FastAPI**, **SQLAlchemy (async)** и **PostgreSQL**.  
Все запросы и ответы проходят через Pydantic-схемы, обеспечивая строгую валидацию данных.

---

## Модели данных

### Chat

| Поле        | Тип       | Описание                  |
|------------|----------|---------------------------|
| id         | int      | Уникальный идентификатор чата |
| title      | str      | Название чата (не пустое, 1-200 символов) |
| created_at | datetime | Дата и время создания     |

### Message

| Поле        | Тип       | Описание                       |
|------------|----------|--------------------------------|
| id         | int      | Уникальный идентификатор сообщения |
| chat_id    | int      | ID чата (FK на Chat)           |
| text       | str      | Текст сообщения (не пустой, 1-5000 символов) |
| created_at | datetime | Дата и время создания          |

Связь: **Chat 1 — N Message**

---

## API

### POST /chats/

**Создание чата**

**Request Body:**

```json
{
  "title": "Название чата"
}
```

**Response:**

```json
{
  "id": 1,
  "title": "Название чата",
  "created_at": "2026-01-27T12:00:00"
}
```

### POST /chats/{id}/messages/

**Отправка сообщения в чат**

**Request Body:**

```json
{
  "text": "Привет, это сообщение!"
}
```

**Response:**

```json
{
  "id": 1,
  "chat_id": 1,
  "text": "Привет, это сообщение!",
  "created_at": "2026-01-27T12:01:00"
}
```

### GET /chats/{id}?limit=10

**Получение чата с последними N сообщениями**

**Response:**

```json
{
{
  "id": 1,
  "title": "Название чата",
  "created_at": "2026-01-27T12:00:00",
  "messages": [
    {
      "id": 1,
      "chat_id": 1,
      "text": "Привет, это сообщение!",
      "created_at": "2026-01-27T12:01:00"
    },
    ...
  ]
}
}
```

### DELETE /chats/{id}

**Удаление чата вместе со всеми сообщениями**

**Response:**

```json
{
  "success": true
}
```

---

## Валидация и ограничения

- **title**: длина 1–200 символов, пробелы по краям обрезаются

- **text**: длина 1–5000 символов, пробелы по краям обрезаются

- **limit**: default = 20, >0, <=100

- Нельзя отправить сообщение в несуществующий чат (возвращается 404)

- При удалении чата все сообщения удаляются каскадно

---

## Запуск проекта

1.  Запуск проекта

Клонируем репозиторий:
```bash
git clone <repo-url>
cd hitalent
```

2. Установим зависимости через Poetry:
```bash
poetry install
```

3. Создать файл окружения:
```bash
cp .env.example .env
```

4. Запуск docker-compose (PostgreSQL + API):
```bash
docker compose up -d --build
```

5. API будет доступно по адресу: ```http://localhost:8000```

---

## Миграции базы данных

- Все миграции хранятся в папке ```alembic/versions```

- Генерация миграции:
```bash
docker compose exec api alembic revision --autogenerate -m "описание"
```

- Применение миграции:
```bash
docker compose exec api alembic upgrade head
```

---

## Тестирование

- Pytest установлен в окружении проекта

- Запуск тестов через ```docker-compose.test.yml```:
``` bash
docker compose -f docker-compose.test.yml up --build
```

- Остановка и удаление контейнеров после тестирования:
``` bash
docker stop hitalent_tests_runner hitalent_test_postgres && docker rm hitalent_tests_runner hitalent_test_postgres
```

- Проверка того, что все контейнеры удалены:
```bash
sudo docker ps -a
```

---

## Линтеры и форматирование кода

В проекте настроены:

- ```black``` — форматирование

- ```isort``` — сортировка импортов

- ```ruff``` — статический анализ кода

**Makefile команды:**
```bash
make run_linters     # проверка чекером black, isort, ruff
make run_formaters   # применяет black и isort
```

Все инструменты игнорируют .venv/, .env и временные файлы.

---

## Docker и docker-compose

- PostgreSQL 15

- API на FastAPI с hot reload

- Контейнеры:
    - db — база данных
    - api — приложение FastAPI

- Подключение к базе:
```bash
docker compose exec api psql -U postgres -d hitalent_db
```

---
