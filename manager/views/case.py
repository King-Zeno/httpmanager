import os,io
from rest_framework.views import APIView
from utils.common import CustomViewBase, JsonResponse
from rest_framework.decorators import action
from manager.models.case import TestStep,TestCase
from manager.serializers.case import (
    TestCaseSerializer,
    TestStepSerializer,
    TestCaseListSerializer
)
from rest_framework_extensions.mixins import NestedViewSetMixin
from django_filters.rest_framework import DjangoFilterBackend
from utils.runner import RunTestCase
from utils.filter import TestCaseFilter


class TestCaseViewSet(CustomViewBase):
    queryset = TestCase.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TestCaseFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TestCaseListSerializer
        return TestCaseSerializer

    def create(self, request, *args, **kwargs):
        try: 
            data = request.data.dict()
        except:
            data = request.data
        username = "%s%s" % (request.user.last_name, request.user.first_name)
        data['author'] = username
        print(data)

        serializer = self.get_serializer(data=data)
        is_valid = serializer.is_valid(raise_exception=True)
        if not is_valid:
            return JsonResponse(code=400, msg=serializer.errors)

        self.perform_create(serializer)
        return JsonResponse(code=200, msg="success", data=serializer.data)

    @action(methods=['get'],detail=True)
    def run(self, request, *args, **kwargs):
        """
        get /?env=pk  环境变量
        """
        object = self.get_object()
        # env = request.data['env']
        env = request.GET.get('env')
        
        results = RunTestCase().run_case(env=env, case_id=object.id)

        return JsonResponse(code=results['code'], data=results['data'], msg=results['msg'])


class TestStepViewSet(NestedViewSetMixin, CustomViewBase):
    serializer_class = TestStepSerializer

    def get_queryset(self):
        case_id = self.get_parents_query_dict()['case_step']
        queryset = TestStep.objects.filter(case=case_id)

        return queryset

    @action(methods=['get'],detail=True)
    def copy(self, request, *args, **kwargs):
        object = self.get_object()
        object.pk= None
        object.save()
        return JsonResponse(code=200, msg="success")


class TestCaseEnvView(APIView):

    def get(self, request, *args):
        data = ""
        env_file = "testcase/.env"
        try:
            with open(env_file, 'r', encoding='utf-8') as stream:
                for line in stream.readlines():
                    data += line;
        except:
            data = ""
        return JsonResponse(code=200,data=data)

    def post(self, request, *args, **kwargs):

        data = request.POST.get('env')
        env_file = "testcase/.env"
        try:
            file_obj = open(env_file, 'w')
            file_obj.write(data)
            file_obj.close()
            return JsonResponse(code=200, data=data, msg="修改成功")
        except:
            return JsonResponse(code=500, msg="修改失败")
