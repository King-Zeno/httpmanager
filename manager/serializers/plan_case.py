from rest_framework import serializers
from manager.models.plan_case import PlanCase

class PlanCaseParamSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanCase
        # fields = '__all__'
        exclude = ['create_time','update_time']

