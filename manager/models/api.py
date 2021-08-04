from django.db import models
from .base import BaseTable
from .project import Project
from .env import EnvParam


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
    author = models.CharField(max_length=50, null=True, blank=True, verbose_name='创建人')
    name = models.CharField(max_length=250, verbose_name='api名称')
    method = models.CharField(choices=METHOD, max_length=20, verbose_name='请求方式')
    url = models.CharField( max_length=250, verbose_name='URL路径')
    headers = models.JSONField(default=dict, null=True, verbose_name='请求头')
    body = models.JSONField(default=dict, null=True, verbose_name='请求参数')

    class Meta:
        verbose_name = "Api"
        db_table = 'api'
