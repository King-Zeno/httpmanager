from rest_framework.viewsets import ModelViewSet
from utils.common import CustomViewBase, JsonResponse
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.plan import Plan
from manager.serializers.plan import PlanParamSerializer, PlanListSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.http import HttpResponse

class PlanParamViewSet(CustomViewBase):
    model = Plan
    queryset = Plan.objects.all()
    serializer_class = PlanParamSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlanListSerializer
        return PlanParamSerializer

    def create(self, request, *args, **kwargs):
        username = "%s%s" % (request.user.last_name, request.user.first_name)
        data = request.data.copy()
        data['author'] = username
        serializer = self.get_serializer(data=data)
        is_valid = serializer.is_valid(raise_exception=True)
        if not is_valid:
            return JsonResponse(code=400, msg=serializer.errors)

        self.perform_create(serializer)
        return JsonResponse(code=200, msg="success", data=serializer.data)