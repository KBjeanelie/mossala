from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.serializers.project_manager_serializer import ApplyProjectSerializer, ProjectEvaluationSerializer, ProjectSerializer
from backend.models.project_manager import Project, ApplyProject, ProjectEvaluation

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
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
        project = self.get_object()
        project.close_project()
        return Response({'status': 'project closed'}, status=status.HTTP_201_CREATED)

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