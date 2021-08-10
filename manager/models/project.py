from django.db import models
from .base import BaseTable

class Project(BaseTable):
    name = models.CharField(max_length=100, verbose_name='项目名')
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='描述')

    class Meta:
        verbose_name = "项目"
        db_table = 'project'
