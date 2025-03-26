"""
URL configuration for mossala project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.app_report_view import FeedBackFromUserCreateView, WarningFromUserCreateView
from api.views.user_manager_view import CurrentUserProjectStatsView
from api.views.worker_view import UserProjectStatsView
from authentication.views import CustomTokenObtainPairView, GetCurrentUserInfo, LogoutAPIView, QuaterListView, RegisterView, WorkerDetailView, WorkerListView
from mossala import settings

schema_view = get_schema_view(
   openapi.Info(
      title="API de Mossala",
      default_version='v0.0.1', 
      description="Documentation de l'API de Mossala",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="eneogroug.cg@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/user/user-project-stats/', CurrentUserProjectStatsView.as_view(), name='user-project-stats'),
    path('api/workers/worker-project-stats/', UserProjectStatsView.as_view(), name='worker-project-stats'),
    path('api/warnings/', WarningFromUserCreateView.as_view(), name='warning-create'),
    path('api/feedbacks/', FeedBackFromUserCreateView.as_view(), name='feedback-create'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/quaters/', QuaterListView.as_view(), name='quaters-list'),
    path('api/user/current/', GetCurrentUserInfo.as_view(), name='current_user'),
    path('api/workers/', WorkerListView.as_view(), name='worker-list'),
    path('api/workers/<int:pk>/', WorkerDetailView.as_view(), name='worker-detail'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
