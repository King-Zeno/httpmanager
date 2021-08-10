from rest_framework import serializers
from manager.models.report import Report
from manager.models.project import Project
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .project import ProjectSerializer

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'
        read_only = True
        #exclude = ['create_time', 'update_time']

class ReportListSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Project.objects.all(),
                fields=('report', 'project'),
                message='该报告已存在同一个项目下'
            )]
        model = Report
        read_only = False
        fields = '__all__'
