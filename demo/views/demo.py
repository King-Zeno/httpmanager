from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from utils.common import CustomViewBase
from rest_framework import filters, serializers
from utils.common import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from demo.serializers.demo import CompanySerializer, WorkerSerializer

from demo.models.company import Company
from demo.models.worker import Worker



class CompanyViewSet(ModelViewSet):
    '''
    list:
        列表 (get /company/)
    Retrieve：
        详情 (get /company/{id}/)
    create
        创建 (post /company/)
    update:
        更新 (put/patch /company/{id}/)
    destroy:
        删除（delete /company/{id}/)
    '''

    queryset = Company.objects.all()      # 指定 queryset 数据
    serializer_class = CompanySerializer   # 指定 serializer

    def list(self, request):
        ''' 列表 '''
        # queryset = Company.objects.all()
        data = self.get_serializer(self.queryset, many=True).data

        # 返回序列化后的数据
        return JsonResponse(data=data, msg="success")

    def retrieve(self, request, *args, **kwargs):
        ''' 详情 '''
        instance = self.get_object()
        data = self.get_serializer(instance).data
         
        return JsonResponse(code=200, msg='success',data=data)

    def create(self, request):
        ''' 创建 '''
        # 获取 POST 过来的数据
        data = request.data
        print(data)
        serializer = self.get_serializer(data=data)
        # 校验
        if serializer.is_valid(raise_exception=True):
            # 保存数据
            serializer.save()
            # 返回
            return JsonResponse(data=serializer.data, msg="success")

        return JsonResponse(msg="fail")

    def update(self, request, *args,**kwargs):
        ''' 更新  '''
        instance = self.get_object()
        data = request.data
        print(data)
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return JsonResponse(data=serializer.data, msg="fail")

    def destroy(self, request, *args, **kwargs):
        '''  删除 '''
        instance = self.get_object
        instance.delete()

        return JsonResponse(msg="success")



class WorkerViewSet(ModelViewSet):
    # 不重写方法只需指定数据库查询的 queryset 和 serializer
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer