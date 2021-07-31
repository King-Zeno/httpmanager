from rest_framework import serializers
from manager.models.plan import Plan

class PlanParamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        # fields = '__all__'
        exclude = ['create_time', 'update_time']
