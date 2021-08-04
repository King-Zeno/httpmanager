from rest_framework.response import Response
from utils.common import CustomViewBase, JsonResponse
from rest_framework.decorators import action
from manager.models.case import TestStep,TestCase
from manager.serializers.case import TestCaseSerializer,TestStepSerializer,TestCaseListSerializer


class TestCaseViewSet(CustomViewBase):
    queryset = TestCase.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestCaseListSerializer
        return TestCaseSerializer



class TestStepViewSet(CustomViewBase):
    serializer_class = TestStepSerializer
    queryset = TestStep.objects.all()
