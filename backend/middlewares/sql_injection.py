import re
from django.http import JsonResponse

class SQLInjectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        blacklist = ["SELECT", "INSERT", "DELETE", "UPDATE", "DROP", "--", ";", " OR ", " AND "]
        for param in request.GET.values():
            if any(word in param.upper() for word in blacklist):
                return JsonResponse({"error": "Requête suspecte détectée"}, status=403)
        return self.get_response(request)
