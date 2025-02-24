from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.serializers.manager_profil_serializer import UserEducationSerializer, UserExperienceSerializer, UserLanguageSerializer, UserPortfolioSerializer, UserRecommendationSerializer
from backend.models.manager_profil import UserExperience, UserEducation, UserLanguage, UserPortfolio, UserRecommendation

class UserExperienceViewSet(viewsets.ModelViewSet):
    queryset = UserExperience.objects.all()
    serializer_class = UserExperienceSerializer
    permission_classes = [IsAuthenticated]

class UserEducationViewSet(viewsets.ModelViewSet):
    queryset = UserEducation.objects.all()
    serializer_class = UserEducationSerializer
    permission_classes = [IsAuthenticated]

class UserLanguageViewSet(viewsets.ModelViewSet):
    queryset = UserLanguage.objects.all()
    serializer_class = UserLanguageSerializer
    permission_classes = [IsAuthenticated]

class UserPortfolioViewSet(viewsets.ModelViewSet):
    queryset = UserPortfolio.objects.all()
    serializer_class = UserPortfolioSerializer
    permission_classes = [IsAuthenticated]

class UserRecommendationViewSet(viewsets.ModelViewSet):
    queryset = UserRecommendation.objects.all()
    serializer_class = UserRecommendationSerializer
    permission_classes = [IsAuthenticated]