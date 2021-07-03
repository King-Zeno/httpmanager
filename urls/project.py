from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from manager.views import project

router = DefaultRouter()

router.register('', project.ProjectViewSet, basename='project')

urlpatterns = [
    re_path('^', include(router.urls)),
]