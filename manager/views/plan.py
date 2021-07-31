from rest_framework.viewsets import ModelViewSet
from utils.common import CustomViewBase
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.plan import Plan
from manager.serializers.plan import PlanParamSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.http import HttpResponse

class PlanParamViewSet(NestedViewSetMixin, CustomViewBase):
    model = Plan
    queryset = Plan.objects.all()
    serializer_class = PlanParamSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)

def index(request):

    #add
    Plan.objects.create(request.body.title())

    #find
    Plan.objects.all()#获取全部数据
    Plan.objects.get()#获取单条数据
    Plan.objects.filter()#获取指定条件的数据，不存在返回None

    #delete
    Plan.objects.filter(id=2).delete()

    #update
    Plan.objects.filter(id=2).update()

    return HttpResponse()