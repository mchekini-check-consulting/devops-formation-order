FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV ENV_NAME=prod
ENV LOG_LEVEL=INFO
ENV OTEL_SERVICE_NAME=order

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn --workers=1 --timeout=300 --config=config/gunicorn.py --bind=0.0.0.0:8000 config.wsgi:application"]