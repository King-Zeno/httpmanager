from manager.models.plan import Plan
from django.db import models
from .base import BaseTable
from .case import TestCase


class Report(BaseTable):
    name = models.CharField(max_length=100, verbose_name='Report')
    path = models.CharField(max_length=100, null=True, blank=True, verbose_name='报告路径')
    case = models.ForeignKey(TestCase, related_name='case_report', null=True,
                                on_delete=models.SET_NULL, db_constraint=False,verbose_name='关联用例')
    plan = models.ForeignKey(Plan, related_name='plan_report', null=True,
                                on_delete=models.SET_NULL, db_constraint=False,verbose_name='关联计划')

    class Meta:
        verbose_name = "报告"
        db_table = 'report'
