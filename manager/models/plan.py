from django.db import models
from .base import BaseTable
from .project import Project
from .case import TestCase
from django.contrib.auth import get_user_model


class Plan(BaseTable):
    name = models.CharField(max_length=40, verbose_name='计划名称')
    desc = models.CharField(max_length=255, null=True,
                            blank=True, verbose_name='描述')
    project = models.ForeignKey(Project, related_name='project_plan',
                                null=True, blank=True, on_delete=models.SET_NULL, db_constraint=False, verbose_name='项目id')
    author = models.CharField(max_length=50, verbose_name='创建人')
    partner = models.JSONField(null=True, verbose_name='关联人')
    project_name = models.CharField( max_length=50, verbose_name='项目名称')

    class Meta:
        verbose_name = "测试计划"
        db_table = 'plan'

class PlanCase(models.Model):
    plan = models.ForeignKey(Plan, related_name='plan_case',
                            db_constraint=False, verbose_name='关联计划', on_delete=models.CASCADE,)
    case = models.ForeignKey(TestCase, related_name='case_testcase',
                             on_delete=models.RESTRICT, db_constraint=False, verbose_name='测试用例')

    class Meta:
        verbose_name = "用例对应计划"
        db_table = 'plan_case'
