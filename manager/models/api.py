from django.db import models
from .base import BaseTable
from .project import Project
from .env import EnvParam


class APICate(models.Model):

    name = models.CharField(max_length=200, verbose_name='分类名称')
    project = models.ForeignKey(Project, related_name='cate_project', 
                                on_delete=models.SET_NULL, null=True, db_constraint=False, verbose_name='关联项目')
    desc = models.CharField(max_length=500, null=True, verbose_name="备注")

    class Meta:
        verbose_name = "APICate"
        db_table = "api_cate"


class Api(BaseTable):

    METHOD = (
        ('get', 'GET'),
        ('post', 'POST'),
        ('put', 'PUT'),
        ('delete', 'DELETE'),
        ('patch', 'PATCH'),
        ('head', 'HEAD'),
        ('options', 'OPTIONS')
    )

    project = models.ForeignKey(Project, related_name='project_api',
                                on_delete=models.CASCADE, db_constraint=False, verbose_name='关联项目')
    cate = models.ForeignKey(APICate, related_name='api_cate',
                             on_delete=models.SET_NULL, null=True, db_constraint=False, verbose_name='分类')
    author = models.CharField(max_length=50, null=True, blank=True, verbose_name='创建人')
    name = models.CharField(max_length=250, verbose_name='api名称')
    method = models.CharField(choices=METHOD, max_length=20, verbose_name='请求方式')
    url = models.CharField( max_length=250, verbose_name='URL路径')
    headers = models.JSONField(default=dict, null=True, verbose_name='请求头')
    body = models.JSONField(default=dict, null=True, verbose_name='请求参数')

    class Meta:
        verbose_name = "Api"
        db_table = 'api'
