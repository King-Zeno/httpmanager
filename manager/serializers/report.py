from rest_framework import serializers
from manager.models.report import Report
from manager.models.project import Project
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .project import ProjectSerializer

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'
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
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        report = Report.objects.create(**(validated_data['report']))
        Project.objects.create(project=validated_data['project'], env=report)
        return validated_data

    def update(self, instance, validated_data):
        report_obj = instance.report
        report_obj.name = validated_data['report']['name']
        report_obj.save()
        return super().update(instance, validated_data)
