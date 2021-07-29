from rest_framework import serializers
from manager.models.api import Api
from utils.common import JsonSerializer

class ApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Api
        fields = '__all__'
