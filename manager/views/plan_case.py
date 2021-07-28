from rest_framework.viewsets import ModelViewSet
from utils.common import CustomViewBase
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.plan_case import Plan_Case
from manager.serializers.plan_case import PlanCaseParamSerializer


class PlanCaseParamViewSet(CustomViewBase):
    queryset = Plan_Case.objects.all()
    serializer_class = PlanCaseParamSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)
