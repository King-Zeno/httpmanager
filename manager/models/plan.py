from django.db import models
from .base import BaseTable
from .project import Project
from .case import TestCase


class Plan(BaseTable):
    name = models.CharField(max_length=40, verbose_name='计划名称')
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name='描述')
    project = models.ForeignKey(Project, related_name='project_plan',
                                null=True, blank=True, on_delete=models.SET_NULL, verbose_name='项目id')
    #case = models.JSONField(null=True, blank=True, on_delete=models.SET_NULL, verbose_name='用例id')
    author = models.CharField(max_length=50, verbose_name='创建人')

    class Meta:
        verbose_name = "测试计划"
        db_table = 'plan'


class PlanCase(BaseTable):
    plan = models.ForeignKey(Plan,
                                related_name='plan', on_delete=models.RESTRICT, db_constraint=False,
                                verbose_name='关联计划')
    case = models.ForeignKey(TestCase,
                            related_name='plan_case', on_delete=models.RESTRICT, db_constraint=False,
                            verbose_name='测试用例')

    class Meta:
        verbose_name = "用例对应计划"
        db_table = 'plan_case'
