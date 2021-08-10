from rest_framework import serializers
from manager.models.plan import Plan, PlanCase
from manager.models.project import Project
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .project import ProjectSerializer

class PlanParamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        # fields = '__all__'
        exclude = ['create_time', 'update_time']

class PlanListSerializer(serializers.ModelSerializer):
    #project = ProjectSerializer()

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Project.objects.all(),
                fields=('plan', 'project'),
                message='该计划已存在同一个项目下'
            )]
        model = Plan
        fields = '__all__'

class PlanCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanCase
        fields = '__all__'