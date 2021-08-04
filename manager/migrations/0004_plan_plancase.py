# Generated by Django 3.2.4 on 2021-07-31 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20210729_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, verbose_name='用例名称')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='描述')),
                ('plan_id', models.IntegerField(verbose_name='计划id')),
                ('case_id', models.IntegerField(verbose_name='用例id')),
                ('author', models.CharField(max_length=50, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '计划用例表',
                'db_table': 'plan_case',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=40, verbose_name='计划名称')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='描述')),
                ('author', models.CharField(max_length=50, verbose_name='创建人')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='manager.project', verbose_name='项目id')),
            ],
            options={
                'verbose_name': '测试计划',
                'db_table': 'plan',
            },
        ),
    ]