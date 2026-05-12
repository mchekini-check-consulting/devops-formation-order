def post_fork(server, worker):
    from config.otel import configure_opentelemetry

    configure_opentelemetry()
