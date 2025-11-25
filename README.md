# Mini CRM API (FastAPI + SQLAlchemy + SQLite + Alembic + Pydantic + Docker + Pytest)

Минимальный сервис распределения входящих обращений между операторами с учётом их веса и нагрузки.
Поддерживает операторов, лидов, источники и обращения.
Из-за ограничения времени выполнения в 3 часа написано минимальное количество функционала, только то что описано в тестовом задании, в т.ч. с применением relationship.

## Функциональность API

### Операторы (Operators)
- POST /operators/ — создать оператора  
- GET /operators/ — список всех операторов  
- PATCH /operators/{operator_id} — изменить лимит нагрузки или активность оператора

- Оператор имеет:  
- имя  
- активен / не активен  
- лимит по максимальной нагрузке  (обращения)
- распределение по источникам (вес) 

### Источники (Sources)
- POST /sources/ — создать источник  
- POST /sources/{id}/weights/ — назначить операторов для источника и указать их веса  
- GET /sources/ — список всех источников  

### Обращения (Contacts)
- POST /contacts/ — зарегистрировать обращение

- Если подходящих операторов нет — обращение создаётся без оператора.

### Статистика (Stats)
- GET /stats/operators/ — операторы с количеством обращений  
- GET /stats/sources/ — источники с количеством обращений  
- GET /stats/distribution/operators/ — ператоры с списком обращений

### Лиды (Leads)
- GET /leads/ — лиды с списком обращений

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
