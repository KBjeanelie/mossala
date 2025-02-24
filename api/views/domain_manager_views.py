from rest_framework import viewsets
from backend.models.domain_manager import Domain, Specialty, Job
from api.serializers.domain_manger_serializer import DomainSerializer, SpecialtySerializer, JobSerializer

class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer