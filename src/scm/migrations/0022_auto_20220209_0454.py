# Generated by Django 3.0.7 on 2022-02-09 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0021_auto_20220209_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qc_report',
            name='color',
            field=models.CharField(blank=True, choices=[(None, '请选择'), ('ONE_C', '单色'), ('ALL_C', '齐色')], default=None, max_length=100, verbose_name='颜色'),
        ),
        migrations.AlterField(
            model_name='qc_report',
            name='product_status',
            field=models.CharField(blank=True, choices=[(None, '请选择'), ('NEW_P', '刚出成品'), ('FINISH_P', '成品全部完成'), ('SEND_P', '大货包装完成')], default=None, max_length=100, verbose_name='大货状态'),
        ),
        migrations.AlterField(
            model_name='qc_report',
            name='ratio',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='抽查比列'),
        ),
    ]
