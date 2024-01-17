# -*- coding: utf-8 -*-
"""
# @Time ： 2023/1/30 14:34
# @Auth ： Mr. royalday 2487625775
# @Site     :
# @File     : serializers.py.py
# @Software : PyCharm
# @Company  ：XXX
# @Function ：
"""
from rest_framework import serializers

from .models import Project
from dvadmin.utils.serializers import CustomModelSerializer


class ProjectModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    statusDESC = serializers.CharField(source="get_status_display")

    class Meta:
        model = Project
        fields = '__all__'


class ProjectModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = Project
        fields = '__all__'


