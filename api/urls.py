from rest_framework.routers import DefaultRouter
from api.views.domain_manager_views import DomainViewSet, SpecialtyViewSet, JobViewSet
from api.views.manager_profil_view import UserEducationViewSet, UserExperienceViewSet, UserLanguageViewSet, UserPortfolioViewSet, UserRecommendationViewSet
from api.views.project_manager_view import ApplyProjectViewSet, ProjectEvaluationViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'domain', DomainViewSet, basename='domain')
router.register(r'specialty', SpecialtyViewSet, basename='specialty')
router.register(r'user-experiences', UserExperienceViewSet, basename='user-experience')
router.register(r'user-educations', UserEducationViewSet, basename='user-education')
router.register(r'user-languages', UserLanguageViewSet, basename='user-language')
router.register(r'user-portfolios', UserPortfolioViewSet, basename='user-portfolio')
router.register(r'user-recommendations', UserRecommendationViewSet, basename='user-recommendation')
router.register(r'job', JobViewSet, basename='job')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'apply-projects', ApplyProjectViewSet, basename='apply-project')
router.register(r'project-evaluations', ProjectEvaluationViewSet, basename='project-evaluation')

urlpatterns = router.urls