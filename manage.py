#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    load_dotenv(".env.local")
    from config.otel import configure_opentelemetry
    configure_opentelemetry()
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
