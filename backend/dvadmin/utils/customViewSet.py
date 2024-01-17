# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/1 001 22:57
@Remark: 自定义视图集
"""
from .json_response import SuccessResponse, ErrorResponse
from .viewset import CustomModelViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action


class MyCustomModelViewSet(CustomModelViewSet):
    """
    自定义的ModelViewSet:
    集成框架的CustomModelViewSet
    """

    keys = openapi.Schema(description='主键列表', type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING)

    def multiple_delete_detail(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['keys'],
        properties={'keys': keys}
    ), operation_summary='批量删除')
    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        return self.multiple_delete_detail(request, *args, **kwargs)
