from datetime import datetime, timezone

from django.db import connection
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

SERVICE_NAME = "order"
DB_TIMEOUT = 2


def health(request):
    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SET statement_timeout = %s", [DB_TIMEOUT * 1000])
            cursor.execute("SELECT 1")
        db_status = "UP"
    except Exception:
        db_status = "DOWN"

    status = "UP" if db_status == "UP" else "DOWN"
    status_code = 200 if status == "UP" else 503
    return JsonResponse(
        {
            "status": status,
            "service": SERVICE_NAME,
            "timestamp": timestamp,
            "checks": {"database": db_status},
        },
        status=status_code,
    )


urlpatterns = [
    path("api/health", health, name="health"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("", include("orders.urls")),
]
