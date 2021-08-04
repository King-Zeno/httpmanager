from django_filters.rest_framework import DjangoFilterBackend
from manager.models.api import Api
from manager.serializers.api import ApiSerializer
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from utils.common import CustomViewBase, JsonResponse
from utils.runner import RunApi


class ApiViewSet(NestedViewSetMixin, CustomViewBase):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer

    def create(self, request, *args, **kwargs):
        username = "%s%s" % (request.user.last_name, request.user.first_name)
        data = request.data
        data['author'] = username
        serializer = self.get_serializer(data=data)
        is_valid = serializer.is_valid(raise_exception=True)
        if not is_valid:
            return JsonResponse(code=400, msg=serializer.errors)

        self.perform_create(serializer)
        return JsonResponse(code=200, msg="success", data=serializer.data)

    @action(methods=['get'], detail=True)
    def run(self, request, *args, **kwargs):
        object = self.get_object()
        env = request.GET.get('env')
        data = RunApi.run(self, env, object.id)

        return Response(data, status=status.HTTP_200_OK)
