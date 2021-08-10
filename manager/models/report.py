from django.db import models
from .base import BaseTable
from .case import TestCase

class Report(BaseTable):
    name = models.CharField(max_length=100, verbose_name='Report')
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='描述')
    path = models.CharField(max_length=100, null=True, blank=True, verbose_name='报告路径')
    case = models.ForeignKey(TestCase, related_name='case', on_delete=models.RESTRICT, db_constraint=False,
                                verbose_name='关联用例')

    class Meta:
        verbose_name = "报告"
        db_table = 'report'