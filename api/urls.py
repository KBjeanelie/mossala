from rest_framework.routers import DefaultRouter
from api.views.domain_manager_views import DomainViewSet, SpecialtyViewSet, JobViewSet
from api.views.project_manager_view import ApplyProjectViewSet, ProjectEvaluationViewSet, ProjectMessageViewSet, ProjectViewSet, ProjectWithApplicationsView
from api.views.user_manager_view import CurrentAssignedUserProjectViewSet, CurrentUserEducationViewSet, CurrentUserExperienceViewSet, CurrentUserProjectViewSet, CurrentUserRealisationViewSet
from api.views.worker_view import AssignedUserProjectViewSet, UserEducationViewSet, UserExperienceViewSet, UserProjectViewSet, UserRealisationViewSet

router = DefaultRouter()
router.register(r'domain', DomainViewSet, basename='domain')
router.register(r'metiers', JobViewSet, basename='metiers')
router.register(r'specialty', SpecialtyViewSet, basename='specialty')
##############################################################################################################################
### User Manager
##############################################################################################################################
#router.register(r'user-experiences', CurrentUserExperienceViewSet, basename='user-experience')
#router.register(r'user-realisations', CurrentUserRealisationViewSet, basename='user-realisation')
#router.register(r'user-educations', CurrentUserEducationViewSet, basename='user-education')
router.register(r'user-assigned-project', CurrentAssignedUserProjectViewSet, basename='user-assigned-project')
router.register(r'user-created-project', CurrentUserProjectViewSet, basename='user-created-project')
##############################################################################################################################
### Worker manager
##############################################################################################################################
#router.register(r'worker-realisations', UserRealisationViewSet, basename='worker-realisation')
#router.register(r'worker-experiences/(?P<user_id>\d+)', UserExperienceViewSet, basename='worker-experience')
#router.register(r'worker-educations/(?P<user_id>\d+)', UserEducationViewSet, basename='worker-education')
router.register(r'worker-assigned-project/(?P<user_id>\d+)', AssignedUserProjectViewSet, basename='worker-assigned-project')
router.register(r'worker-created-project/(?P<user_id>\d+)', UserProjectViewSet, basename='worker-created-project')
##############################################################################################################################
### Project manager
##############################################################################################################################
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'apply-projects', ApplyProjectViewSet, basename='apply-project')
router.register(r'project-messages', ProjectMessageViewSet, basename='project-messages')
#router.register(r'project-evaluations', ProjectEvaluationViewSet, basename='project-evaluation')

urlpatterns = router.urls


from django.urls import include, path
urlpatterns += [
    path('projects/<int:project_id>/applications/', ProjectWithApplicationsView.as_view(), name='project-with-applications'),
]