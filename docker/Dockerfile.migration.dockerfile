FROM python:3.12.0-slim-bookworm

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

WORKDIR /app

# Copy requirements.txt and install them first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD alembic upgrade head && echo 'Migration completed'