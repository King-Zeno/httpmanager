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

    def create(self, validated_data):
        env = EnvParam.objects.create(
            name=validated_data['env']['name'], key=validated_data['env']['key'], value=validated_data['env']['value'])
        ProjectEnv.objects.create(project=validated_data['project'], env=env)
        return validated_data

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=ProjectEnv.objects.all(),
                fields=('project', 'env'),
                message='该项目已存在相同的环境'
            )]
        model = ProjectEnv
        fields = ['id', 'project', 'env']


class ProjectSerializer(serializers.ModelSerializer):
    project_env = ProjectEnvSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
