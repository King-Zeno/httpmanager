from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from demo.views import demo

router = DefaultRouter()

router.register('company', demo.CompanyViewSet, basename='company')
router.register('worker', demo.WorkerViewSet, basename='worker')

urlpatterns = [
    re_path('^', include(router.urls)),
]