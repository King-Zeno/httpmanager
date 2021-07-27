from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter

from manager.views import project, env

router = ExtendedDefaultRouter()
router.register(r'project', project.ProjectViewSet, basename='project').register(
    r'env', project.ProjectEnvViewSet, basename='project-env', parents_query_lookups=['project'])

router.register('env', env.EnvParamViewSet, basename='env')


urlpatterns = [
    re_path('^', include(router.urls)),
]
