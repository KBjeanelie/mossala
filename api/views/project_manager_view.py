from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from api.serializers.project_manager_serializer import ApplyProjectSerializer, ProjectEvaluationSerializer, ProjectImageSerializer, ProjectMessageSerializer, ProjectSerializer
from backend.models.project_manager import Project, ApplyProject, ProjectEvaluation, ProjectImage, ProjectMessage
from rest_framework.exceptions import PermissionDenied

class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    permission_classes = [IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('is_closed')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        print(request.data)  # Affiche les données reçues
        print(request.FILES)  # Affiche les fichiers reçus
        # Extraire les données des images
        uploaded_images = request.FILES.getlist('uploaded_images')
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            project = serializer.save(owner=request.user)

            for image in uploaded_images:
                ProjectImage.objects.create(project=project, image=image)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            print(f"Erreur lors de la création du projet: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='by-specialty')
    def list_by_specialty(self, request):
        user = request.user
        specialties = user.specialty.all()
        projects = Project.objects.filter(specialty__in=specialties).distinct()
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_freelancer(self, request, pk=None):
        project = self.get_object()
        freelancer_id = request.data.get('freelancer_id')
        try:
            freelancer = User.objects.get(id=freelancer_id)
            project.assigned_freelancer = freelancer
            project.close_project
            project.save()
            return Response({'status': 'freelancer assigned'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'freelancer not found'}, status=404)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        project_id = request.data['id']
        try:
            project = Project.objects.get(id=project_id)
            project.close_project()
            return Response({'status': 'project closed'}, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            return Response({'error': 'project not found'}, status=404)
    
    @action(detail=False, methods=['get'], url_path='is-open')
    def isOpen(self, request):
        user = request.user
        projects = Project.objects.filter(owner=user, is_closed=False)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApplyProjectViewSet(viewsets.ModelViewSet):
    queryset = ApplyProject.objects.all()
    serializer_class = ApplyProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrer les candidatures pour ne retourner que celles liées au projet spécifié
        et appartenant à l'utilisateur connecté.
        """
        project_id = self.request.query_params.get('project_id')
        
        if not project_id:
            return ApplyProject.objects.none()
        
        try:
            project = Project.objects.get(id=project_id)
            return ApplyProject.objects.filter(project=project, user=self.request.user)
        except Project.DoesNotExist:
            return ApplyProject.objects.none()
    
    def create(self, request):
        """
        Créer une candidature et l'associer à l'utilisateur connecté.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Mettre à jour une candidature uniquement si elle appartient à l'utilisateur connecté.
        """
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à modifier cette candidature.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Supprimer une candidature uniquement si elle appartient à l'utilisateur connecté.
        """
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer cette candidature.")
        return super().destroy(request, *args, **kwargs)    



        # Retourner les données du projet et des candidatures
        return Response({
            "project": project_serializer.data,
            "applications": applications_serializer.data
        }, status=status.HTTP_200_OK)

class ProjectWithApplicationsView(APIView):
    """
    Vue pour récupérer un projet donné avec toutes ses candidatures.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, *args, **kwargs):
        try:
            # Récupérer le projet par son ID
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise NotFound("Le projet demandé n'existe pas.")

        # Récupérer toutes les candidatures associées au projet
        applications = ApplyProject.objects.filter(project=project)
        applications_serializer = ApplyProjectSerializer(applications, many=True)

        # Retourner les données du projet et des candidatures
        return Response({
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "amount": project.amount,
                "adress": project.adress,
                "owner": project.owner.username,
                "is_closed": project.is_closed,
                "created_at": project.created_at,
            },
            "applications": applications_serializer.data
        })


class ProjectMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les messages entre le client et le freelance.
    """
    serializer_class = ProjectMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retourne les messages liés à un projet pour l'utilisateur connecté.
        """
        project_id = self.request.query_params.get('project_id')
        if not project_id:
            return ProjectMessage.objects.none()

        try:
            project = Project.objects.get(id=project_id)
            if self.request.user != project.owner and not ApplyProject.objects.filter(project=project, user=self.request.user).exists():
                raise PermissionDenied("Vous n'êtes pas autorisé à accéder à cette discussion.")
            return ProjectMessage.objects.filter(project=project)
        except Project.DoesNotExist:
            return ProjectMessage.objects.none()

    def perform_create(self, serializer):
        """
        Crée un message et vérifie que l'utilisateur est autorisé à envoyer un message pour ce projet.
        """
        project = serializer.validated_data['project']

        # Vérifier si l'utilisateur est le propriétaire du projet
        if self.request.user == project.owner:
            serializer.save(sender=self.request.user)
            return

        # Vérifier si l'utilisateur a postulé au projet
        if ApplyProject.objects.filter(project=project, user=self.request.user).exists():
            serializer.save(sender=self.request.user)
            return

        # Si l'utilisateur n'est ni le propriétaire ni un freelance ayant postulé, refuser l'accès
        raise PermissionDenied("Vous n'êtes pas autorisé à envoyer un message pour ce projet.")


class ProjectEvaluationViewSet(viewsets.ModelViewSet):
    queryset = ProjectEvaluation.objects.all()
    serializer_class = ProjectEvaluationSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['get'], url_path='by-specialty')
    def list_by_specialty(self, request):
        user = request.user
        specialties = user.specialty.all()
        projects = Project.objects.filter(specialty__in=specialties).distinct()
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)