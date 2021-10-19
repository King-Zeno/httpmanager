from rest_framework import fields, serializers
from manager.models.case import TestStep, TestCase
from .report import ReportListSerializer

class TestCaseSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    report = ReportListSerializer(many=True, source="case_report")
    class Meta:
        model = TestCase
        fields = '__all__'


class TestStepSerializer(serializers.ModelSerializer):
    include_case = TestCaseSerializer(source='testcase', read_only=True)
    class Meta:
        model = TestStep
        fields = '__all__'


class TestCaseListSerializer(serializers.ModelSerializer):
    case_step = TestStepSerializer(many=True, required=False)            #返回结果集
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = TestCase
        fields = '__all__'
