from rest_framework import serializers
from backend.models.project_manager import Project, ApplyProject, ProjectEvaluation, ProjectImage

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_at', 'owner',]

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        specialties = validated_data.pop('specialty', [])
        
        project = Project.objects.create(**validated_data)
        
        if specialties:
            project.specialty.set(specialties)

        # Associe les images au projet
        for image in uploaded_images:
            ProjectImage.objects.create(project=project, image=image)

        return project

class ApplyProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyProject
        fields = '__all__'

class ProjectEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEvaluation
        fields = '__all__'