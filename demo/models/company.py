from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100,unique=True, verbose_name='公司名')
    address = models.CharField(max_length=500, null=True, verbose_name='公司地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "公司表"
        db_table = 'company'