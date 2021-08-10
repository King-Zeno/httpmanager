from django.db import models
from .base import BaseTable

class Report(BaseTable):
    name = models.CharField(max_length=100, verbose_name='Report')
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='描述')
    path = models.CharField(max_length=100, null=True, blank=True, verbose_name='报告')

    class Meta:
        verbose_name = "报告"
        db_table = 'report'
