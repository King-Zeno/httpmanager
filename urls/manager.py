from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter

from manager.views import project, env, plan, plan_case

router = ExtendedDefaultRouter()
router.register(r'project', project.ProjectViewSet, basename='project').register(
    r'env', project.ProjectEnvViewSet, basename='project-env', parents_query_lookups=['project'])

router.register('env', env.EnvParamViewSet, basename='env')

router.register('plan', plan.PlanParamViewSet, basename='plan')

router.register('plan_case', plan_case.PlanCaseParamViewSet, basename='plan_case')


urlpatterns = [
    re_path('^', include(router.urls)),
]
