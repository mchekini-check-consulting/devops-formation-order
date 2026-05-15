import os


def configure_opentelemetry():
    """
    Configure Azure Monitor OpenTelemetry si la connection string est définie.

    Active automatiquement :
    - L'auto-instrumentation Django (un span par requête HTTP)
    - La propagation W3C traceparent entre services
    - L'export des traces et logs vers Application Insights
    - La remontée automatique des exceptions non capturées
    """
    connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")

    if not connection_string:
        return

    from azure.monitor.opentelemetry import configure_azure_monitor

    configure_azure_monitor(
        connection_string=connection_string,
        service_name="order",
        service_version="1.0.0",
    )


def attach_otel_log_handlers():
    """
    Attache le handler OpenTelemetry aux loggers Python.
    Doit être appelé APRÈS que Django ait appliqué sa config LOGGING
    (sinon dictConfig écrase nos handlers).
    """
    connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")

    if not connection_string:
        return

    import logging

    from opentelemetry._logs import get_logger_provider
    from opentelemetry.sdk._logs import LoggingHandler

    otel_handler = LoggingHandler(logger_provider=get_logger_provider())

    for logger_name in ("orders"):
        lg = logging.getLogger(logger_name)
        lg.addHandler(otel_handler)
