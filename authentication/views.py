from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from authentication.serializer import CustomTokenObtainPairSerializer, RegisterSerializer, UserSerializer
from .models import User, UserStatus
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        role = UserStatus.objects.get(status=request.data['status'].lower())
        request.data['status'] = [role.id]
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