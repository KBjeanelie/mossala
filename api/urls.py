from rest_framework.routers import DefaultRouter
from api.views.domain_manager_views import DomainViewSet, SpecialtyViewSet, JobViewSet

router = DefaultRouter()
router.register(r'domain', DomainViewSet, basename='domain')
router.register(r'specialty', SpecialtyViewSet, basename='specialty')
router.register(r'job', JobViewSet, basename='job')

urlpatterns = router.urls