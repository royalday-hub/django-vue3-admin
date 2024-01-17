# Create your views here.
from .models import Group, GroupModule, GroupCase, GroupStep
from .serializersGroup import GroupSerializer, GroupModuleModelSerializer, GroupModelCreateUpdateSerializer, \
    GroupCaseModelSerializer, GroupCaseModelCreateUpdateSerializer, \
    GroupStepModelSerializer, GroupStepModelCreateUpdateSerializer, GroupModuleModelCreateUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GroupModuleFilter
from ..utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from ..utils.customViewSet import MyCustomModelViewSet


class GroupModelViewSet(MyCustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Group.statusManager.all()
    serializer_class = GroupSerializer
    create_serializer_class = GroupModelCreateUpdateSerializer
    update_serializer_class = GroupModelCreateUpdateSerializer
    filter_fields = ['name', 'project', 'type']


class GroupModuleModelViewSet(MyCustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = GroupModule.statusManager.all()
    serializer_class = GroupModuleModelSerializer
    create_serializer_class = GroupModuleModelCreateUpdateSerializer
    update_serializer_class = GroupModuleModelCreateUpdateSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = GroupModuleFilter

    # search_fields = ['name', 'group']

    def create(self, request, *args, **kwargs):
        # 根据传参不同判断是 模块排序 还是 新增模块
        if request.data.get("toSort", False):
            for sort_index, module_id in enumerate(request.data.get("data")):
                groupModuleObj = GroupModule.objects.filter(id=module_id).first()
                groupModuleObj.sort = sort_index
                groupModuleObj.save()
            return DetailResponse(data=None, msg="操作成功")
        else:
            serializer = self.get_serializer(data=request.data, request=request)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return DetailResponse(data=serializer.data, msg="新增成功")


class GroupCaseModelViewSet(MyCustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = GroupCase.statusManager.all()
    serializer_class = GroupCaseModelSerializer
    create_serializer_class = GroupCaseModelCreateUpdateSerializer
    update_serializer_class = GroupCaseModelCreateUpdateSerializer
    filter_fields = ['name', 'module']

    def create(self, request, *args, **kwargs):
        # 根据传参不同判断是 模块排序 还是 新增模块
        if request.data.get("toSort", False):
            data = request.data.get("data", {})
            caseStepDic = data.get("caseStepDic", {})
            caseList = data.get("caseList", [])
            for case_sort_index, case_id in enumerate(caseList):
                groupCaseObj = GroupCase.objects.filter(id=case_id).first()
                groupCaseObj.sort = case_sort_index
                groupCaseObj.save()
                for step_sort_index, step_id in enumerate(caseStepDic.get(str(case_id), [])):
                    groupStepObj = GroupStep.objects.filter(id=step_id).first()
                    groupStepObj.sort = step_sort_index
                    groupStepObj.save()
            return DetailResponse(data=None, msg="操作成功")
        else:
            serializer = self.get_serializer(data=request.data, request=request)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return DetailResponse(data=serializer.data, msg="新增成功")

    def destroy(self, request, *args, **kwargs):
        del_type = request.data.get("type", 0)
        del_id = request.data.get("id", -1)
        print(del_type, del_id)
        # 1: 用例， 2步骤
        if del_type == 1:
            instance = self.get_object()
            instance.delete()
        elif del_type == 2:
            GroupStep.objects.filter(id=del_id).delete()
        else:
            ErrorResponse(msg="类型错误")

        return DetailResponse(data=[], msg="删除成功")

    def multiple_delete_detail(self, request, *args, **kwargs):
        request_data = request.data
        casList = request_data.get('casList', None)
        stepList = request_data.get('stepList', None)
        if casList or stepList:
            b = self.get_queryset().filter(id__in=casList).delete()
            a = GroupStep.objects.filter(id__in=stepList).delete()
            print(a, casList)
            print(b, stepList)
            return SuccessResponse(data=[], msg="删除成功")
        else:
            return ErrorResponse(msg="请勾选需要删除的记录")


class GroupStepModelViewSet(MyCustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = GroupStep.statusManager.all()
    serializer_class = GroupStepModelSerializer
    create_serializer_class = GroupStepModelCreateUpdateSerializer
    update_serializer_class = GroupCaseModelCreateUpdateSerializer
    filter_fields = ['name', ]
