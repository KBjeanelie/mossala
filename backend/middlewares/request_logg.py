import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"[{datetime.now()}] Requête {request.method} sur {request.path}")
        response = self.get_response(request)
        logger.info(f"[{datetime.now()}] Réponse {response.status_code} pour {request.path}")
        return response
