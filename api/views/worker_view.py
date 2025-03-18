from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.serializers.manager_profil_serializer import UserEducationSerializer, UserExperienceSerializer
from api.serializers.project_manager_serializer import ProjectSerializer
from authentication.models import User
from backend.models.manager_profil import UserEducation, UserExperience
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

