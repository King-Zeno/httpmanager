# Generated by Django 3.2.4 on 2021-08-23 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_auto_20210811_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='partner',
            field=models.JSONField(null=True, verbose_name='关联人'),
        ),
    ]