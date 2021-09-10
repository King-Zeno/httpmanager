from utils.common import CustomViewBase, JsonResponse
from rest_framework import filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from manager.models.project import Project
from manager.models.env import ProjectEnv
from manager.models.api import Api
from manager.serializers.project import ProjectSerializer, ProjectEnvSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin
from utils.runner import import_api


class ProjectViewSet(NestedViewSetMixin, CustomViewBase):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = (permissions.IsAuthenticated,)

    @action(methods=['get'], detail=False)
    def method(self, request, *args, **kwargs):
        data = Api.METHOD
        return JsonResponse(code=200, data=data)

    @action(methods=['post'], detail=True)
    def upload(self, request, *args, **kwargs):
        author = "%s%s" % (request.user.last_name, request.user.first_name)
        object = self.get_object()
        file_obj = request.FILES.get('file', None)
        try:
            import_api(object.id, file_obj, author)
            return JsonResponse(code=200, msg="导入成功")
        except Exception as e:
            print(e)
            return JsonResponse(code=502, msg="导入失败")


class ProjectEnvViewSet(NestedViewSetMixin, CustomViewBase):
    queryset = ProjectEnv.objects.all()
    serializer_class = ProjectEnvSerializer

    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        env_obj = object.env
        object.delete()
        env_obj.delete()
        return JsonResponse(code=200, msg="删除成功")
