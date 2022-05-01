"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view, openapi

from authapp.views import AppUserViewSet
from userworkapp.views import ProjectViewSet, UserWorkingProjectViewSet, ExecutorViewSet, ToDoViewSet, \
    SwaggerTemplateView, RedocTemplateView, ToDoViewSetBase, UserOnProjectById
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register('users', AppUserViewSet, basename='users')
router.register('project', ProjectViewSet)
router.register('user_working_project', UserWorkingProjectViewSet)
router.register('executor', ExecutorViewSet)
router.register('todo', ToDoViewSet)
router.register('todo/base', ToDoViewSetBase)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),

    path('graphql', GraphQLView.as_view(graphiql=True)),
    path('users/', AppUserViewSet.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('openapi', get_schema_view(openapi.Info(title='MyProject',
                                                 default_version='2.0',
                                                 description='API for Project',
                                                 version='2.0')).as_view(), name='openapi-schema'),
    # Swagger
    path('swagger-ui/', SwaggerTemplateView.as_view(), name='swagger-ui'),
    # ReDoc
    path('redoc-ui/', RedocTemplateView.as_view(), name='redoc-ui'),
    # GraphQl
#    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
