from django.shortcuts import render


from .models import KeyWord
from ..utils.customViewSet import MyCustomModelViewSet
from .serializersKeyWord import KeyWordSerializer, KeyWordModelCreateUpdateSerializer


class KeyWordModelViewSet(MyCustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = KeyWord.statusManager.all()
    serializer_class = KeyWordSerializer
    create_serializer_class = KeyWordModelCreateUpdateSerializer
    update_serializer_class = KeyWordModelCreateUpdateSerializer
    filter_fields = ['name', 'type', 'key']
