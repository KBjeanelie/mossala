from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from backend.models.app_report import WarningFromUser, FeedBackFromUser
from api.serializers.app_report_serializer import WarningFromUserSerializer, FeedBackFromUserSerializer

class WarningFromUserCreateView(generics.CreateAPIView):
    """
    Vue pour créer un avertissement par l'utilisateur connecté.
    """
    serializer_class = WarningFromUserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FeedBackFromUserCreateView(generics.CreateAPIView):
    """
    Vue pour créer un feedback par l'utilisateur connecté.
    """
    serializer_class = FeedBackFromUserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)