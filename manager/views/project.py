from utils.common import CustomViewBase, JsonResponse
from rest_framework import filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.project import Project
from manager.models.env import ProjectEnv
from manager.serializers.project import ProjectSerializer, ProjectEnvSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin


class ProjectViewSet(NestedViewSetMixin, CustomViewBase):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = (permissions.IsAuthenticated,)


class ProjectEnvViewSet(NestedViewSetMixin, CustomViewBase):
    queryset = ProjectEnv.objects.all()
    serializer_class = ProjectEnvSerializer

    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        env_obj = object.env
        object.delete()
        env_obj.delete()
        return JsonResponse(code=200, msg="删除成功")
