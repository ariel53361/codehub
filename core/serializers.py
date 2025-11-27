from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserReadAndUpdateSerializer(BaseUserSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username',
                  'email', 'first_name', 'last_name']


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
