import logging
import traceback
import uuid

logger = logging.getLogger("orders")


class RequestLoggingMiddleware:
    """
    Middleware qui log chaque requête entrante et sortante en JSON structuré.

    - Extrait le correlationId depuis le header X-Correlation-ID (ou en génère un)
    - Extrait le userId depuis le header X-User-ID si présent
    - Log la requête entrante (method, path)
    - Log la réponse (method, path, status_code)
    - Log les exceptions avec exception.type, exception.message, exception.stackTrace
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        correlation_id = request.headers.get(
            "X-Correlation-ID", str(uuid.uuid4())
        )
        user_id = request.headers.get("X-User-ID", "anonymous")

        request.correlation_id = correlation_id
        request.user_id_header = user_id

        logger.info(
            "Incoming request",
            extra={
                "correlationId": correlation_id,
                "userId": user_id,
                "httpMethod": request.method,
                "httpPath": request.path,
            },
        )

        response = self.get_response(request)

        logger.info(
            "Request completed",
            extra={
                "correlationId": correlation_id,
                "userId": user_id,
                "httpMethod": request.method,
                "httpPath": request.path,
                "httpStatusCode": response.status_code,
            },
        )

        return response

    def process_exception(self, request, exception):
        correlation_id = getattr(request, "correlation_id", "unknown")
        user_id = getattr(request, "user_id_header", "anonymous")

        logger.error(
            "Unhandled exception",
            extra={
                "correlationId": correlation_id,
                "userId": user_id,
                "httpMethod": request.method,
                "httpPath": request.path,
                "exception.type": type(exception).__name__,
                "exception.message": str(exception),
                "exception.stackTrace": traceback.format_exc(),
            },
        )
        return None
