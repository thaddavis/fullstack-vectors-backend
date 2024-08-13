# TLDR

Anomaly Detection

## Development log

- https://alembic.sqlalchemy.org/en/latest/

- Install alembic>=1.13.2,<2.0
  - pip install -r requirements.txt

- alembic init alembic
  - https://alembic.sqlalchemy.org/en/latest/tutorial.html#creating-an-environment

- https://alembic.sqlalchemy.org/en/latest/index.html

## CREATING DB + MIGRATIONS FROM SCRATCH

- docker run --name fullstack-rag -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

- docker exec -ti fullstack-rag createdb -U postgres fullstack_rag

- alembic init alembic

- alembic revision -m "create user table"
  - populate upgrade/downgrade functions

- alembic upgrade head

- docker network connect agent-network fullstack-rag

- FYI: docker exec -ti fullstack-rag psql -U postgres -d fullstack_rag

- alembic revision -m "create chat_history table"
  - populate upgrade/downgrade functions

- alembic upgrade head

- OOPS: alembic downgrade -1

- alembic upgrade head

- FYI: alembic history
- FYI: alembic current
- FYI: alembic upgrade +1

- https://alembic.sqlalchemy.org/en/latest/autogenerate.html

- alembic/env.py and edit LINES 7 & 23

- alembic revision --autogenerate -m "create logins table"

- alembic upgrade head

## Writing to the logins table

- https://fastapi.tiangolo.com/tutorial/background-tasks/#create-a-task-function

## Resetting PROD db and running migrations

