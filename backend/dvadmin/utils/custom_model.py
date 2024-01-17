# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/5 20:28
@Auth ： Mr. royalday 2487625775
# @Site     : 
# @File     : custom_model.py
# @Software : PyCharm
# @Company  ：XXX
# @Function ：
"""
from django.db.models import QuerySet
from django.db import models

from dvadmin.utils.models import CoreModel


class StatusQuerySet(QuerySet):
    pass


class StatusManager(models.Manager):
    """仅筛选启用状态的记录"""

    def __init__(self, *args, **kwargs):
        self.__add_is_del_filter = False
        super(StatusManager, self).__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        # 考虑是否主动传入is_deleted
        if not kwargs.get('is_deleted') is None:
            self.__add_is_del_filter = True
        return super(StatusManager, self).filter(*args, **kwargs)

    def get_queryset(self):
        if self.__add_is_del_filter:
            return StatusManager(self.model, using=self._db).exclude(is_deleted=False)
        # 不展示状态为禁用的
        return StatusQuerySet(self.model).exclude(is_deleted=True).exclude(status=0)

    def get_by_natural_key(self, name):
        return StatusQuerySet(self.model).get(username=name)


class MyCoreModel(CoreModel):
    """
    在核心字段的基础性上添加状态字段
    """
    statusManager = StatusManager()
    STATUS_CHOICES = (
        (0, "禁用"),
        (1, "启用"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="状态", help_text="状态")

    class Meta:
        abstract = True
        verbose_name = '状态模型'
        verbose_name_plural = verbose_name
