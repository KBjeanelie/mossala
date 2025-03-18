from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.serializers.manager_profil_serializer import UserEducationSerializer, UserExperienceSerializer
from api.serializers.project_manager_serializer import ProjectSerializer
from backend.models.manager_profil import UserEducation, UserExperience
from backend.models.project_manager import Project

class CurrentUserProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(owner=user)

class CurrentAssignedUserProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(assigned_freelancer=user)


class CurrentUserExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = UserExperienceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return UserExperience.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.save()
    
    def perform_update(self, serializer, instance):
        serializer.save(user=self.request.user)
        return serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()
        return "Experience deleted successfully"

class CurrentUserEducationViewSet(viewsets.ModelViewSet):
    serializer_class = UserEducationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return UserEducation.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.save()
        
    def perform_update(self, serializer, instance):
        serializer.save(user=self.request.user)
        return serializer.save()
        
    def perform_destroy(self, instance):
        instance.delete()
        return "Education deleted successfully"

