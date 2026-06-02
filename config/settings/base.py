import os
from pathlib import Path

from corsheaders.defaults import default_headers

from config.logging import LOGGING  # noqa: F401 — utilisé par Django

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "orders.apps.OrdersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "orders.middleware.RequestLoggingMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASE_ROUTERS = ["config.db_router.ReadWriteRouter"]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "UNAUTHENTICATED_USER": None,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Order Service API",
    "DESCRIPTION": "Microservice de gestion des commandes",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
CORS_ALLOW_HEADERS = [
    *default_headers,
    "x-correlation-id",
    "x-user-id",
]

APPEND_SLASH = True
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
