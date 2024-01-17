from django.shortcuts import render

# Create your views here.

from .models import Project
from .serializers import ProjectModelCreateUpdateSerializer, ProjectModelSerializer
from ..utils.customViewSet import MyCustomModelViewSet
from dvadmin.utils.json_response import SuccessResponse


class ProjectModelViewSet(MyCustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    create_serializer_class = ProjectModelCreateUpdateSerializer
    update_serializer_class = ProjectModelCreateUpdateSerializer
    filter_fields = ['name', 'parents', 'status']
    search_fields = ['name', 'parents']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        exclude_self = request.GET.get('self')
        if exclude_self:
            queryset = queryset.exclude(id=eval(exclude_self))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")


class ProjectSelectModelViewSet(MyCustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Project.statusManager.all()
    serializer_class = ProjectModelSerializer
    filter_fields = ['name', ]
