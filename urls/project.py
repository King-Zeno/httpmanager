from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework_extensions.routers import ExtendedDefaultRouter

from manager.views import project, env, api

router = ExtendedDefaultRouter()
project_router = router.register(r'project', project.ProjectViewSet, basename='project')
project_router.register(r'env', project.ProjectEnvViewSet, basename='project-env', parents_query_lookups=['project'])
project_router.register('api', api.ApiViewSet, basename='project-api',parents_query_lookups=['project'])

urlpatterns = [
    re_path('^', include(router.urls)),
]