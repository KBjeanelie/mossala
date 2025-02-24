from rest_framework import serializers
from backend.models.project_manager import Project, ApplyProject, ProjectEvaluation

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ApplyProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyProject
        fields = '__all__'

class ProjectEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEvaluation
        fields = '__all__'