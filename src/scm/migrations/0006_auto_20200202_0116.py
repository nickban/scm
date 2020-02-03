# Generated by Django 3.0.2 on 2020-02-02 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0005_auto_20200202_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='status',
            field=models.CharField(blank=True, choices=[('NEW', '新建'), ('SENT_F', '送工厂'), ('COMPLETED', '完成')], default='NEW', max_length=50, verbose_name='样板状态'),
        ),
    ]
