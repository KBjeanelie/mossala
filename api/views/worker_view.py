from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers.manager_profil_serializer import UserEducationSerializer, UserExperienceSerializer, UserRealisationSerializer
from api.serializers.project_manager_serializer import ProjectSerializer
from authentication.models import User
from backend.models.manager_profil import UserEducation, UserExperience, UserRealisation
from backend.models.project_manager import Project

class UserProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        return Project.objects.filter(owner=user)

class AssignedUserProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        return Project.objects.filter(assigned_freelancer=user)


class UserExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = UserExperienceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        return UserExperience.objects.filter(user=user)
    
class UserEducationViewSet(viewsets.ModelViewSet):
    serializer_class = UserEducationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        return UserEducation.objects.filter(user=user)


class UserRealisationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les réalisations des utilisateurs.
    """
    serializer_class = UserRealisationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtrer les réalisations pour ne retourner que celles de l'utilisateur connecté.
        """
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        return UserRealisation.objects.filter(user=user)


class UserProjectStatsView(APIView):
    """
    Vue pour renvoyer le nombre de projets créés et assignés pour l'utilisateur connecté.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        created_projects_count = Project.objects.filter(owner=user).count()
        assigned_projects_count = Project.objects.filter(assigned_freelancer=user).count()

        return Response({
            "created_projects_count": created_projects_count,
            "assigned_projects_count": assigned_projects_count
        })