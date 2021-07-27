
from rest_framework import serializers
from manager.models.env import EnvParam

class EnvParamSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnvParam
        # fields = '__all__'
        exclude = ['create_time','update_time']

