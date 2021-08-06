from rest_framework.viewsets import ModelViewSet
from utils.common import CustomViewBase
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.plan import Plan
from manager.serializers.plan import PlanParamSerializer, TestPlanListSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.http import HttpResponse

class PlanParamViewSet(CustomViewBase):
    model = Plan
    queryset = Plan.objects.all()
    serializer_class = PlanParamSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestPlanListSerializer
        return PlanParamSerializer