
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ListSerializer):
    last_login = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_joined = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, label="密码", write_only=True, required=False)

    class Meta:
        model = User
        fields = '__all__'
