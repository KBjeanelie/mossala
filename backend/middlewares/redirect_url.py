from django.shortcuts import redirect
from django.conf import settings

class RedirectIfNotAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"URL demandée : {request.path}")

        # Liste des pages accessibles sans être connecté
        public_urls = [settings.LOGIN_URL, 'api/register/', '/admin/login/']

        # Vérifier si l'utilisateur n'est PAS connecté et qu'il ne demande PAS une page publique
        if not request.user.is_authenticated and request.path not in public_urls:
            print("Utilisateur NON connecté, redirection vers /login/")
            return redirect(settings.LOGIN_URL)  # Redirection correcte
        
        print("Utilisateur connecté ou URL publique, accès autorisé.")
        response = self.get_response(request)  # Exécuter la vue
        return response
