from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self):
        from config.otel import attach_otel_log_handlers

        attach_otel_log_handlers()
