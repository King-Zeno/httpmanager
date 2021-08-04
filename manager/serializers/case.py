from rest_framework import fields, serializers
from manager.models.case import TestStep, TestCase


class TestStepSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestStep
        fields = '__all__'


class TestCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestCase
        fields = '__all__'


class TestCaseListSerializer(serializers.ModelSerializer):
    case_step = TestStepSerializer(many=True, required=False)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = TestCase
        fields = '__all__'
