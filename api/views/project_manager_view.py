from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.serializers.project_manager_serializer import ApplyProjectSerializer, ProjectEvaluationSerializer, ProjectImageSerializer, ProjectSerializer
from backend.models.project_manager import Project, ApplyProject, ProjectEvaluation, ProjectImage

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
    
    @action(detail=False, methods=['get'], url_path='by-specialty')
    def list_by_specialty(self, request):
        user = request.user
        specialties = user.specialty.all()
        projects = Project.objects.filter(specialty__in=specialties).distinct()
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

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