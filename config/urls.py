from django.db import connection
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def health(request):
    try:
        connection.ensure_connection()
        db_status = "up"
    except Exception:
        db_status = "down"
        return JsonResponse({"status": "unhealthy", "database": db_status}, status=503)
    return JsonResponse({"status": "healthy", "database": db_status})


urlpatterns = [
    path("api/orders/health", health, name="health"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("", include("orders.urls")),
]
