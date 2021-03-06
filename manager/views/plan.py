from rest_framework.viewsets import ModelViewSet
from utils.common import CustomViewBase
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.plan import Plan
from manager.serializers.plan import PlanParamSerializer


class PlanParamViewSet(CustomViewBase):
    queryset = Plan.objects.all()
    serializer_class = PlanParamSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)
