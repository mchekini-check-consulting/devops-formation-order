def configure_opentelemetry():
    """
    Configure un TracerProvider OpenTelemetry local, sans export vers un
    backend APM (Application Insights n'est plus disponible).

    Active :
    - L'auto-instrumentation Django (un span par requête HTTP)
    - Des traceId/spanId réels dans les logs (config/logging.py), pour
      corréler les requêtes sans dépendre d'un service de tracing externe
    """
    from opentelemetry import trace
    from opentelemetry.instrumentation.django import DjangoInstrumentor
    from opentelemetry.sdk.trace import TracerProvider

    trace.set_tracer_provider(TracerProvider())
    DjangoInstrumentor().instrument()
