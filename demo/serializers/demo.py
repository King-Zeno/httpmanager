from django.core.checks import messages
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
from demo.models import company
from demo.models import worker
from demo.models.company import Company
from demo.models.worker import Worker


class WorkerSerializer(serializers.ModelSerializer):
    
    # 自定义字段
    company_name = serializers.ReadOnlyField(source="company.name")

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Worker.objects.all(),
                fields=['name','company'],
                message="该公司下已存在该名员工"
            )]
        model = Worker
        fields = ['id', 'name', 'sex', 'age', 'company', 'company_name']

    
class CompanySerializer(serializers.ModelSerializer):
    # 序列化公司下的员工
    company_worker = WorkerSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'address','company_worker']
        # fields = '__all__'

    # 数据校验
    def validate(self, data):
        name = data['name']
        if (name >= u'\u0041' and name < u'\u005b') or (name >= u'\u0061' and name < u'\u007b') or (name >= u'\u0030' and name < u'\u0040'):
            return data
        raise serializers.ValidationError("请输入英文加数字的非特殊字符")

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

