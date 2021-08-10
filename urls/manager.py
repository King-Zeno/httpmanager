from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter, ExtendedSimpleRouter

from manager.views import project, env, api, plan, case, report

router = ExtendedDefaultRouter()
project_router = router.register(r'project', project.ProjectViewSet, basename='project')
project_router.register(r'env', project.ProjectEnvViewSet, basename='project-env', parents_query_lookups=['project'])
project_router.register('api', api.ApiViewSet, basename='project-api',parents_query_lookups=['project'])
project_router.register(r'plans',
                        plan.PlanParamViewSet,
                        basename='project-plan',
                        parents_query_lookups=['project']) \
    .register(r'case',
              case.TestCaseViewSet,
              basename='project-plans-case',
              parents_query_lookups=['name', 'project'])
router.register('case', case.TestCaseViewSet, basename='case').register(
    'step', case.TestStepViewSet, basename='case-step', parents_query_lookups=['case_step'])

router.register('env', env.EnvParamViewSet, basename='env')
router.register('report', report.ReportViewSet, basename='report')


urlpatterns = [
    re_path('^', include(router.urls)),
]
