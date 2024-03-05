# ARES

## How it's built

* python -m venv venv
* pip freeze | Out-File -Encoding UTF8 requirements.txt

* alembic init migrations
* alembic revision --autogenerate -m "Database creation"

## How to run

### On production

* sudo docker-compose --env-file .env -f .\docker\docker-compose.yml up -d --build

### On dev

* sudo docker-compose --env-file .env -f .\docker\docker-compose.yml up -d --build
* uvicorn main:app --reload
