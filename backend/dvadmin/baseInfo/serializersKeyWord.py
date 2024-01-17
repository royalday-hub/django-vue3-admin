from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import as_serializer_error

from .models import KeyWord
from dvadmin.utils.serializers import CustomModelSerializer


class KeyWordSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = KeyWord
        fields = "__all__"


class KeyWordModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = KeyWord
        fields = '__all__'
