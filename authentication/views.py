import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from authentication.serializer import CustomTokenObtainPairSerializer, QuaterSerializer, RegisterSerializer, UserSerializer, WorkerSerializer
from .models import Quater, User, UserStatus
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': RegisterSerializer(user, context=self.get_serializer_context()).data,
            'message': 'Utilisateur créé avec succès.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)



class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            user = User.objects.get(tel=request.data["tel"])

            # Récupérer l'IP
            user_ip = self.get_client_ip(request)
            user.last_ip = user_ip

            # Récupérer la localisation
            user.last_location = self.get_location(user_ip)

            # Récupérer l'IMEI envoyé par le client
            user.imei = request.data.get("imei", None)  # Vérifier si l'IMEI est envoyé

            user.save()

        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_location(self, ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            return data["city"]
        except:
            return None
    


class LogoutAPIView(generics.GenericAPIView):
    """
    Endpoint pour déconnecter un utilisateur en blacklistant son token d'accès.
    L'utilisateur doit être authentifié.
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        return None

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except (TokenError, InvalidToken):
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class GetCurrentUserInfo(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(self.serializer_class(user).data)


class UpdateCurrentUserInfo(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    
    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user.save()
        return Response(self.serializer_class(user).data)
    

class WorkerListView(generics.ListAPIView):
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_superuser=False).order_by("-date_joined")


class WorkerDetailView(generics.RetrieveAPIView):
    """
    Vue pour afficher les détails d'un worker spécifique.
    """
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
