import os
import traceback
from datetime import datetime, timezone

from opentelemetry import trace
from pythonjsonlogger.json import JsonFormatter

# ---------------------------------------------------------------------------
# Variables d'environnement pour le logging
# ---------------------------------------------------------------------------
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
SERVICE_NAME = "order"
ENV_NAME = os.environ.get("ENV_NAME", "local")


# ---------------------------------------------------------------------------
# Formatter JSON personnalisé
# ---------------------------------------------------------------------------
class StructuredJsonFormatter(JsonFormatter):
    """
    Surcharge de JsonFormatter pour injecter automatiquement :
    - timestamp (ISO 8601)
    - level (INFO, ERROR, …)
    - service / env (identité du microservice)
    - traceId / spanId (contexte OpenTelemetry)
    - exception.type / exception.message / exception.stackTrace (si erreur)
    """

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        # Champs obligatoires
        log_record["timestamp"] = datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S.%f"
        )[:-3] + "Z"
        log_record["level"] = record.levelname
        log_record["service"] = SERVICE_NAME
        log_record["env"] = ENV_NAME

        # Contexte OpenTelemetry (traceId / spanId)
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx and ctx.trace_id:
            log_record["traceId"] = format(ctx.trace_id, "032x")
            log_record["spanId"] = format(ctx.span_id, "016x")
        else:
            log_record["traceId"] = "00000000000000000000000000000000"
            log_record["spanId"] = "0000000000000000"

        # Exception (si présente)
        if record.exc_info and record.exc_info[0] is not None:
            exc_type, exc_value, exc_tb = record.exc_info
            log_record["exception.type"] = exc_type.__name__
            log_record["exception.message"] = str(exc_value)
            log_record["exception.stackTrace"] = "".join(
                traceback.format_exception(exc_type, exc_value, exc_tb)
            )


# ---------------------------------------------------------------------------
# Configuration LOGGING Django
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": StructuredJsonFormatter,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "orders": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
}
