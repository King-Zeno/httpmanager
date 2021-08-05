from rest_framework import serializers
from manager.models.plan import Plan

class PlanParamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        # fields = '__all__'
        exclude = ['create_time', 'update_time']

class TestPlanListSerializer(serializers.ModelSerializer):
    plan_case = PlanParamSerializer(many=True, required=False)            #返回结果集
    case_name = serializers.CharField(source='case.name', read_only=True)

    class Meta:
        model = Plan
        fields = '__all__'
