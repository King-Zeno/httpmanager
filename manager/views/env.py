from rest_framework.viewsets import ModelViewSet
from utils.common import CustomViewBase
from rest_framework import filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.env import EnvParam
from manager.serializers.env import EnvParamSerializer


class EnvParamViewSet(CustomViewBase):
    queryset = EnvParam.objects.all()
    serializer_class = EnvParamSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)
    permission_classes = (permissions.IsAuthenticated,)