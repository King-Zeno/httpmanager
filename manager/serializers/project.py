from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from manager.models.project import Project

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        # validators = [
        #     UniqueValidator(
        #         queryset=Project.objects.all(),
        #         message='项目已存在'
        #     )]
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
