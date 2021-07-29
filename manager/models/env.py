from django.db import models
from .base import BaseTable
from .project import Project


class EnvParam(models.Model):
    # 项目环境变量
    name = models.CharField(max_length=100, verbose_name='变量名称')
    base_url = models.CharField(max_length=200, verbose_name='base url')
    headers = models.JSONField(default=dict, null=True, verbose_name='公共头')
    variables = models.JSONField(default=dict, null=True, verbose_name='公共参数')

    class Meta:
        verbose_name = "环境变量"
        db_table = 'env'


class ProjectEnv(models.Model):
    # db_constraint=False 仅在代码层实现关联，数据库不生成外键
    project = models.ForeignKey(Project, 
                related_name='project_env', on_delete=models.RESTRICT, db_constraint=False, verbose_name='关联项目')
    env = models.ForeignKey(EnvParam,
                related_name='env_param',on_delete=models.RESTRICT, db_constraint=False, verbose_name='关联环境变量')

    class Meta:
        verbose_name = "项目对应环境"
        db_table = 'project_env'
