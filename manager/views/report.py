import os
from rest_framework import filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from utils.common import CustomListViewSet, JsonResponse
from rest_framework.decorators import action
from manager.models.report import Report
from manager.serializers.report import ReportSerializer


class ReportViewSet(CustomListViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        path = object.path
        if os.path.exists(path):
            os.remove(path)
        object.delete()
        return JsonResponse(code=200, msg="删除成功")