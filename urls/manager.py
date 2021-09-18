from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedDefaultRouter, ExtendedSimpleRouter

from manager.views import project, env, api, plan, case, report

router = ExtendedDefaultRouter()
project_router = router.register(r'project', project.ProjectViewSet, basename='project')
project_router.register(r'env', project.ProjectEnvViewSet, basename='project-env', parents_query_lookups=['project'])
project_router.register('api', api.ApiViewSet, basename='project-api',parents_query_lookups=['project'])

plan_router = router.register(r'plan', plan.PlanViewSet, basename='project-plan') 
plan_router.register('case', plan.PlanCaseViewSet, basename='plan-case', parents_query_lookups=['plan']) 
plan_router.register('report', report.ReportViewSet, basename='plan-report', parents_query_lookups=['plan'])

case_router = router.register('case', case.TestCaseViewSet, basename='case') 
case_router.register('step', case.TestStepViewSet, basename='case-step', parents_query_lookups=['case_step']) 
case_router.register('report', report.ReportViewSet, basename='case-report', parents_query_lookups=['case'])

router.register('env', env.EnvParamViewSet, basename='env')
router.register('report', report.ReportViewSet, basename='report')
router.register('cate', api.APICateViewSet, basename='cate')


urlpatterns = [
    path('case/env/',case.TestCaseEnvView.as_view(),name='case-env'),
    re_path('^', include(router.urls)),
]
