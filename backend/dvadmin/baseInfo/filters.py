# -*- coding: utf-8 -*-
"""
# @Time ： 2023/3/26 2:32
# @Auth ： Mr. royalday 2487625775
# @Site     :
# @File     : filters.py
# @Software : PyCharm
# @Company  ：XXX
# @Function ：
"""
from django_filters import rest_framework as filters
from .models import GroupModule


class GroupModuleFilter(filters.FilterSet):
    group = filters.CharFilter(field_name="group__id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = GroupModule
        fields = ['name', 'group']

