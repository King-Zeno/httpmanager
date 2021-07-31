from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter

from manager.views import project, env, api, plan, plan_case

router = ExtendedDefaultRouter()
project_router = router.register(r'project', project.ProjectViewSet, basename='project')\
    .register(r'plans',
              plan.PlanParamViewSet,
              basename='project-plan',
              parents_query_lookups=['project'])\
    .register(r'plan_case',
              plan_case.PlanCaseParamViewSet,
              basename='project-plans-case',
              parents_query_lookups=['author', 'case_id'])
#project_router.register(r'env', project.ProjectEnvViewSet, basename='project-env', parents_query_lookups=['project'])
#project_router.register(r'api', api.ApiViewSet, basename='project-api', parents_query_lookups=['project-api'])


urlpatterns = router.urls