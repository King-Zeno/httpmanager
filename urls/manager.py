from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter

from manager.views import project, env, api, plan, case

router = ExtendedDefaultRouter()
project_router = router.register(r'project', project.ProjectViewSet, basename='project')
project_router.register(r'env', project.ProjectEnvViewSet, basename='project-env', parents_query_lookups=['project'])
project_router.register('api', api.ApiViewSet, basename='project-api',parents_query_lookups=['project'])

router.register('case', case.TestCaseViewSet, basename='case').register(
    'step', case.TestStepViewSet, basename='case-step', parents_query_lookups='case_step')

router.register('env', env.EnvParamViewSet, basename='env')
router.register('plan', plan.PlanParamViewSet, basename='plan')


urlpatterns = [
    re_path('^', include(router.urls)),
]
