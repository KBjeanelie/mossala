from rest_framework import serializers
from authentication.serializer import UserSerializer
from backend.models.project_manager import Project, ApplyProject, ProjectEvaluation, ProjectImage, ProjectMessage

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
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = ApplyProject
        fields = '__all__'
        read_only_fields = ['application_date', 'user']
    
    def create(self, validated_data):
        # Récupérer l'utilisateur depuis le contexte de la requête
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user

        # Créer l'instance ApplyProject avec les données validées
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Récupérer l'utilisateur depuis le contexte de la requête
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user

        # Mettre à jour l'instance ApplyProject avec les données validées
        return super().update(instance, validated_data)
    
    def destroy(self, instance):
        # Récupérer l'utilisateur depuis le contexte de la requête
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if instance.user!= request.user:
                raise serializers.ValidationError("Vous n'êtes pas autorisé à supprimer cette candidature.")

        # Supprimer l'instance ApplyProject
        return super().destroy(instance)
    

class ProjectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMessage
        fields = ['id', 'project', 'sender', 'receiver', 'content', 'timestamp']
        read_only_fields = ['sender', 'timestamp']

class ProjectEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEvaluation
        fields = '__all__'