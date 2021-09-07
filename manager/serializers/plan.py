from rest_framework import fields, serializers
from manager.models.plan import Plan, PlanCase
from .case import TestCaseListSerializer


class PlanCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanCase
        fields = '__all__'


class PlanCaseListSerializer(serializers.ModelSerializer):
    case = TestCaseListSerializer()

    class Meta:
        model = PlanCase
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    class Meta:
        model = Plan
        fields = '__all__'


class PlanListSerializer(serializers.ModelSerializer):
    #反序列化，可增加需要反序列的字段
    plan_case = PlanCaseListSerializer(many=True, required=False, read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    class Meta:
        model = Plan
        fields = '__all__'
