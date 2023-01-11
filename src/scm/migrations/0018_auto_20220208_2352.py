# Generated by Django 3.0.7 on 2022-02-08 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0017_auto_20220208_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qc_report',
            name='color',
            field=models.CharField(choices=[(None, '请选择'), ('ONE_C', '单色'), ('ALL_C', '齐色')], default=None, max_length=100, null=True, verbose_name='颜色'),
        ),
        migrations.AlterField(
            model_name='qc_report',
            name='product_status',
            field=models.CharField(choices=[(None, '请选择'), ('NEW_P', '刚出成品'), ('FINISH_P', '成品全部完成'), ('SEND_P', '大货包装完成')], default=None, max_length=100, null=True, verbose_name='大货状态'),
        ),
        migrations.AlterField(
            model_name='qc_report',
            name='ratio',
            field=models.CharField(max_length=50, null=True, verbose_name='抽查比列'),
        ),
    ]
