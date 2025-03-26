from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.serializers.manager_profil_serializer import UserEducationSerializer, UserExperienceSerializer, UserRealisationSerializer
from api.serializers.project_manager_serializer import ProjectSerializer
from backend.models.manager_profil import UserEducation, UserExperience, UserRealisation
from backend.models.project_manager import Project

class CurrentUserProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(owner=user).order_by('is_closed')

class CurrentAssignedUserProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(assigned_freelancer=user).order_by('is_closed')


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


class CurrentUserRealisationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les réalisations des utilisateurs.
    """
    serializer_class = UserRealisationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtrer les réalisations pour ne retourner que celles de l'utilisateur connecté.
        """
        user = self.request.user
        return UserRealisation.objects.filter(user=user).order_by('-date')

    def perform_create(self, serializer):
        """
        Assigner l'utilisateur connecté à la réalisation lors de sa création.
        """
        
        try :
            serializer.save(user=self.request.user)
            return serializer.save()
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

    def perform_destroy(self, instance):
        """
        Supprimer une réalisation uniquement si elle appartient à l'utilisateur connecté.
        """
        if instance.user == self.request.user:
            instance.delete()
            return Response(status=204)  # No content status code
        else:
            return Response({"error": "You can only delete your own realisation."}, status=403)


class CurrentUserProjectStatsView(APIView):
    """
    Vue pour renvoyer le nombre de projets créés et assignés pour l'utilisateur connecté.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        created_projects_count = Project.objects.filter(owner=user).count()
        assigned_projects_count = Project.objects.filter(assigned_freelancer=user).count()

        return Response({
            "created_projects_count": created_projects_count,
            "assigned_projects_count": assigned_projects_count
        })