from django.db import models
from .base import BaseTable
from .project import Project


class EnvParam(BaseTable):
    name = models.CharField(max_length=250, verbose_name='变量名称')
    key = models.CharField(max_length=50, verbose_name='key')
    value = models.CharField(max_length=250, verbose_name='value')

    class Meta:
        verbose_name = "环境变量"
        db_table = 'env_param'


class ProjectEnv(models.Model):
    # db_constraint=False 仅在代码层实现关联，数据库不生成外键
    project = models.ForeignKey(Project, 
                related_name='project_env', on_delete=models.RESTRICT, db_constraint=False, verbose_name='关联项目')
    env = models.ForeignKey(EnvParam,
                related_name='env_param',on_delete=models.RESTRICT, db_constraint=False, verbose_name='关联环境变量')

    class Meta:
        verbose_name = "项目对应环境"
        db_table = 'project_env'
