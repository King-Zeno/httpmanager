from django.db import models
from .base import BaseTable

class Plan(BaseTable):
    name = models.CharField(max_length=40, verbose_name='计划名称')
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name='描述')
    project_id = models.IntegerField(max_length=11,verbose_name='项目id')
    author = models.CharField(max_length=50, verbose_name='创建人')

    class Meta:
        verbose_name = "测试计划"
        db_table = 'Plan'