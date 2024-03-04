# ARES

## How it's built

* python -m venv venv
* pip freeze | Out-File -Encoding UTF8 requirements.txt

* alembic init migrations
* alembic revision --autogenerate -m "Database creation"


## How to run

### On production
* alembic upgrade head
* gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:10050
* docker-compose up --build

### On dev
* uvicorn main:app --reload
