import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
os.environ.setdefault("DJANGO_SECRET_KEY", "ci-secret-key")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "*")


def pytest_configure():
    if not settings.configured:
        django.setup()
