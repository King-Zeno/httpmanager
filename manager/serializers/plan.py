from rest_framework import serializers
from manager.models.plan import Plan
from manager.models.project import Project
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .project import ProjectSerializer

class PlanParamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        # fields = '__all__'
        exclude = ['create_time', 'update_time']

class TestPlanListSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Project.objects.all(),
                fields=('plan', 'project'),
                message='该计划已存在同一个项目下'
            )]
        model = Plan
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        plan = Plan.objects.create(**(validated_data['plan']))
        Project.objects.create(project=validated_data['project'], env=plan)
        return validated_data

    def update(self, instance, validated_data):
        plan_obj = instance.plan
        plan_obj.name = validated_data['plan']['name']
        plan_obj.base_url = validated_data['plan']['base_url']
        plan_obj.headers = validated_data['plan']['headers']
        plan_obj.variables = validated_data['plan']['variables']
        plan_obj.save()
        return super().update(instance, validated_data)
