def post_fork(server, worker):
    from config.otel import attach_otel_log_handlers, configure_opentelemetry

    configure_opentelemetry()
    attach_otel_log_handlers()
