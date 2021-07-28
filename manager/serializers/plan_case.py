from rest_framework import serializers
from manager.models.plan_case import Plan_Case

class PlanCaseParamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan_Case
        # fields = '__all__'
        exclude = ['create_time','update_time']

