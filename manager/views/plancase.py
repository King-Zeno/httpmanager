from rest_framework.viewsets import ModelViewSet
from utils.common import CustomViewBase
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.plancase import PlanCase
from manager.serializers.plancase import PlanCaseParamSerializer


class PlanCaseParamViewSet(CustomViewBase):
    queryset = PlanCase.objects.all()
    serializer_class = PlanCaseParamSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)
