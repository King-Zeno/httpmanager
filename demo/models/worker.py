from django.db import models
from .company import Company

class Worker(models.Model):
    name = models.CharField(max_length=100,unique=True, verbose_name='职工名')
    sex = models.CharField(max_length=50, null=True, verbose_name='性别')
    age = models.IntegerField(null=True, verbose_name='年龄')
    company = models.ForeignKey(Company, related_name='company_worker', on_delete=models.CASCADE, verbose_name='所属公司')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "职工表"
        db_table = 'worker'