from django.db.models import fields
from rest_framework import serializers
from manager.models.api import Api,APICate
from rest_framework.validators import  UniqueTogetherValidator


class APICateSerializer(serializers.ModelSerializer):

    class Meta:
        model = APICate
        fields = '__all__'

class ApiSerializer(serializers.ModelSerializer):
    cate_name = serializers.CharField(source="cate.name", read_only=True)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=APICate.objects.all(),
                fields=('project', 'name'),
                message='该项目已存在相同的分类'
            )]
        model = Api
        fields = '__all__'
