FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

#CMD ["gunicorn", "config.wsgi:application", "workers:1", "timeout=300", "--bind", "0.0.0.0:8000"]
CMD ["gunicorn", "--workers=1", "--timeout=300", "--bind=0.0.0.0:8000", "config.wsgi:application"]