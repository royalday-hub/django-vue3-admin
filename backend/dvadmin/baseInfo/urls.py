# -*- coding: utf-8 -*-
"""
# @Time ： 2023/1/30 14:41
# @Auth ： Mr. royalday 2487625775
# @Site     :
# @File     : urls.py.py
# @Software : PyCharm
# @Company  ：XXX
# @Function ：
"""
from django.urls import path
from rest_framework.routers import SimpleRouter

from .viewsProject import ProjectModelViewSet, ProjectSelectModelViewSet
from .viewsGroup import GroupModuleModelViewSet, GroupCaseModelViewSet, GroupStepModelViewSet, GroupModelViewSet
from .viewsKeyWord import KeyWordModelViewSet

router = SimpleRouter()
router.register(r"project", ProjectModelViewSet)
router.register(r"groupModule", GroupModuleModelViewSet)
router.register(r"groupModuleCase", GroupCaseModelViewSet)
router.register(r"groupModuleCaseStep", GroupStepModelViewSet)
router.register(r"group", GroupModelViewSet)
router.register(r"keyword", KeyWordModelViewSet)

urlpatterns = [

    path('project/select/', ProjectSelectModelViewSet.as_view({'get': 'list'})),

    # path('case/export/', casesViews.StepModelViewSet.as_view({'post': 'export_data', })),
    # path('case/import/', casesViews.StepModelViewSet.as_view({'get': 'import_data', 'post': 'import_data'})),
    #
    # path('case/chart/', casesViews.CaseChartModelViewSet.as_view({'get': 'list'})),
]
urlpatterns += router.urls
