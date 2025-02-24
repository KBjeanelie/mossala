from rest_framework.routers import DefaultRouter
from api.views.domain_manager_views import DomainViewSet, SpecialtyViewSet, JobViewSet
from api.views.project_manager_view import ApplyProjectViewSet, ProjectEvaluationViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'domain', DomainViewSet, basename='domain')
router.register(r'specialty', SpecialtyViewSet, basename='specialty')
router.register(r'job', JobViewSet, basename='job')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'apply-projects', ApplyProjectViewSet, basename='apply-project')
router.register(r'project-evaluations', ProjectEvaluationViewSet, basename='project-evaluation')

urlpatterns = router.urls