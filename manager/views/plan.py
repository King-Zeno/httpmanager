from rest_framework.viewsets import ModelViewSet
from utils.common import CustomViewBase, JsonResponse
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.plan import Plan, PlanCase
from manager.serializers.plan import (
    PlanCaseSerializer,
    PlanSerializer,
    PlanListSerializer,
    PlanCaseListSerializer
)
from rest_framework_extensions.mixins import NestedViewSetMixin
from utils.common import JsonResponse


class PlanViewSet(CustomViewBase):
    model = Plan
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlanListSerializer
        return PlanSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.dict()
        username = "%s%s" % (request.user.last_name, request.user.first_name)
        data['author'] = username

        serializer = self.get_serializer(data=data)
        is_valid = serializer.is_valid(raise_exception=True)
        if not is_valid:
            return JsonResponse(code=400, msg=serializer.errors)

        self.perform_create(serializer)
        return JsonResponse(code=200, msg="success", data=serializer.data)


class PlanCaseViewSet(NestedViewSetMixin, CustomViewBase):

    queryset = PlanCase.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlanCaseListSerializer
        return PlanCaseSerializer
