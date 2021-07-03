from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from utils.common import CustomViewBase
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.project import Project
from manager.serializers.project import ProjectSerializer


class ProjectViewSet(CustomViewBase):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs) 