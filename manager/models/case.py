from requests.api import request
from manager.models.api import Api
from manager.models.project import Project
from django.db import models
from .base import BaseTable


class TestCase(BaseTable):
    name = models.CharField(max_length=250, verbose_name='测试用例名称')
    project = models.ForeignKey(Project, related_name='project_case',
                                db_constraint=False, on_delete=models.CASCADE, verbose_name='关联项目')
    variables = models.JSONField(null=True, verbose_name="variables")
    parameters = models.JSONField(null=True, verbose_name="parameters")
    export = models.JSONField(null=True, verbose_name="export")

    class Meta:
        verbose_name = "测试用例"
        db_table = 'test_case'


class TestStep(models.Model):
    case = models.ForeignKey(TestCase, related_name='case_step',
                             db_constraint=False,  on_delete=models.CASCADE, verbose_name="测试用例")
    name = models.CharField(max_length=250, verbose_name="接口名称")
    variables = models.JSONField(null=True, verbose_name="variables")
    request = models.JSONField(default=dict, null=True, verbose_name="请求参数")
    testcase = models.ForeignKey(TestCase, related_name='test_case', null=True,
                                 db_constraint=False,  on_delete=models.SET_NULL, verbose_name="用例引用")
    extract = models.JSONField(null=True, verbose_name="提取数据")
    validate = models.JSONField(default=list, null=True, verbose_name="断言校验")
    export = models.JSONField(null=True, verbose_name="export")
    sort = models.IntegerField(default=0, null=True, verbose_name="排序")

    class Meta:
        verbose_name = "测试步骤"
        db_table = 'test_step'
        ordering = ['sort', 'id']
