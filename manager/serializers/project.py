from django.db.models import fields
from django.db import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from manager.models.project import Project
from manager.models.env import ProjectEnv
from manager.models.env import EnvParam
from .env import EnvParamSerializer


class ProjectEnvSerializer(serializers.ModelSerializer):
    env = EnvParamSerializer()

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=ProjectEnv.objects.all(),
                fields=('project', 'env'),
                message='该项目已存在相同的环境'
            )]
        model = ProjectEnv
        fields = ['id', 'project', 'env']

    def create(self, validated_data):
        env = EnvParam.objects.create(**(validated_data['env']))
        ProjectEnv.objects.create(project=validated_data['project'], env=env)
        return validated_data

    def update(self, instance, validated_data):
        env_obj = instance.env
        env_obj.name = validated_data['env']['name']
        env_obj.base_url = validated_data['env']['base_url']
        env_obj.headers = validated_data['env']['headers']
        env_obj.variables = validated_data['env']['variables']
        env_obj.save()
        return validated_data


class ProjectSerializer(serializers.ModelSerializer):
    project_env = ProjectEnvSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
