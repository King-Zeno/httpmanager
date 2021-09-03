from rest_framework import serializers
from manager.models.report import Report
from rest_framework.validators import UniqueTogetherValidator

class ReportSerializer(serializers.ModelSerializer):
    case_name = serializers.CharField(source='case.name', read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Report.objects.all(),
                fields=('plan', 'case', 'path'),
                message='当天报告已存在'
            )]
        model = Report
        fields = '__all__'
