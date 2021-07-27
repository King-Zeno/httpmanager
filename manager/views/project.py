from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes, action
from utils.common import CustomListViewSet, CustomViewBase, JsonResponse
from rest_framework import filters, serializers
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.project import Project
from manager.models.env import ProjectEnv
from manager.serializers.project import ProjectSerializer, ProjectEnvSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin


class ProjectViewSet(NestedViewSetMixin, CustomViewBase):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)



class ProjectEnvViewSet(NestedViewSetMixin, CustomViewBase):
    queryset = ProjectEnv.objects.all()
    serializer_class = ProjectEnvSerializer
