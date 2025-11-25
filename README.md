# Mini CRM API (FastAPI + SQLAlchemy + SQLite + Alembic + Pydantic + Docker + Pytest)

Минимальный сервис распределения входящих обращений между операторами с учётом их веса и нагрузки.
Поддерживает операторов, лидов, источники и обращения.

## Функциональность API

### Операторы (Operators)
- POST /operators/ — создать оператора  
- GET /operators/ — список всех операторов  
- PATCH /operators/{operator_id} — изменить лимит нагрузки или активность оператора  

### Источники (Sources)
- POST /sources/ — создать источник  
- POST /sources/{id}/weights/ — назначить операторов для источника и указать их веса  
- GET /sources/ — список всех источников  

### Обращения (Contacts)
- POST /contacts/ — зарегистрировать обращение  

## Быстрый старт (Docker Compose)
```bash
docker compose up -d
docker compose exec api alembic upgrade head
```
http://localhost:8000/docs

## Запуск тестов 
```bash
docker compose exec api pytest -v -s   
```

## Adminer (управление базой данных)
http://localhost:8080 
(данные для подключения в env файле)

## Alembic (миграция базы данных)
```bash
docker compose exec api alembic revision --autogenerate -m "(название)"
docker compose exec api alembic upgrade head  
```
