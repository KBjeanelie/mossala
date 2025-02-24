from rest_framework import serializers
from backend.models.domain_manager import Domain, Specialty, Job

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'

class SpecialtySerializer(serializers.ModelSerializer):
    domain = DomainSerializer()

    class Meta:
        model = Specialty
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    specialty = SpecialtySerializer()

    class Meta:
        model = Job
        fields = '__all__'