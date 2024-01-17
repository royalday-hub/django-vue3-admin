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
from .models import Group, GroupModule, GroupCase, GroupStep
from dvadmin.utils.serializers import CustomModelSerializer


class GroupSerializer(CustomModelSerializer):
    """
    序列化器
    """
    typeDESC = serializers.CharField(source="get_type_display")
    count = serializers.SerializerMethodField(read_only=True)
    nodeName = serializers.SerializerMethodField()
    nodeId = serializers.SerializerMethodField()

    def get_count(self, instance=None):
        count = 0
        for _module in instance.groupModule.all():
            count += _module.groupCase.count()
        return count

    def get_nodeName(self, instance=None):
        return "123"

    def get_nodeId(self, instance=None):
        return "nodeId"

    class Meta:
        model = Group
        fields = [
            "id", "name", "project", "type", "typeDESC", "description", "creator_name", "count",
            "nodeId", "nodeName"
        ]


class GroupModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = Group
        fields = '__all__'


class GroupModuleModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    moduleName = serializers.CharField(source="name")

    class Meta:
        model = GroupModule
        fields = ["id", "moduleName", "sort", "group", "create_datetime"]
        ordering = ['sort', "-create_datetime"]


class GroupModuleModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = GroupModule
        fields = '__all__'


class GroupStepModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    keywordName = serializers.CharField(source="keyword.name", read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    typeWithId = serializers.SerializerMethodField(read_only=True)
    parent = serializers.CharField(source='case.id',read_only=True)

    def get_type(self, instance=None):
        # 1是用例， 2是步骤
        return 2

    def get_typeWithId(self, instance=None):
        return f"2_{instance.id}"

    class Meta:
        model = GroupStep
        fields = ["id", "name", "keyword", "keywordName", "input_one", "input_two", "input_three",
                  "sort", "creator_name", "create_datetime", "type", "typeWithId", "parent"]
        ordering = ['sort', "-create_datetime"]


class GroupStepModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = GroupStep
        fields = '__all__'


class GroupCaseModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    groupStep = GroupStepModelSerializer(many=True)
    type = serializers.SerializerMethodField(read_only=True)
    typeWithId = serializers.SerializerMethodField(read_only=True)
    parent = serializers.SerializerMethodField(read_only=True)

    def get_typeWithId(self, instance=None):
        # 1是用例， 2是步骤
        return f"2_{instance.id}"

    def get_type(self, instance=None):
        # 1是用例， 2是步骤
        return 1

    def get_typeWithId(self, instance=None):
        return f"1_{instance.id}"

    def get_parent(self, instance=None):
        # 1是用例， 2是步骤
        return "-1"

    class Meta:
        model = GroupCase
        fields = '__all__'
        # fields = ["id", "sort", "creator", "create_datetime", "steps"]
        ordering = ['sort', "-create_datetime"]


class GroupCaseModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = GroupCase
        fields = '__all__'
