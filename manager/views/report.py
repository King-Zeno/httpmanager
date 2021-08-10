from rest_framework import filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from utils.common import CustomListViewSet, JsonResponse
from rest_framework.decorators import action
from manager.models.report import Report
from manager.serializers.report import ReportSerializer, ReportListSerializer


class ReportViewSet(CustomListViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = (permissions.IsAuthenticated,)
    '''def get_serializer_class(self):
        if self.action == 'retrieve':
            return ReportListSerializer
        return ReportSerializer'''

    def destroy(self, request, *args, **kwargs):
        object = self.get_object()

        object.delete()
        return JsonResponse(code=200, msg="删除成功")