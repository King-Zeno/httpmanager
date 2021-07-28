from django.db import models
from .base import BaseTable

class Plan_Case(BaseTable):
    name = models.CharField(max_length=100, verbose_name='用例名称')
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name='描述')
    plan_id = models.IntegerField(max_length=11, verbose_name='计划id')
    case_id = models.IntegerField(max_length=11, verbose_name='用例id')
    author = models.CharField(max_length=50, verbose_name='创建人')

    class Meta:
        verbose_name = "计划用例表"
        db_table = 'Plan_Case'