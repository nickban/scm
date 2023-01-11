# Generated by Django 3.0.7 on 2022-02-09 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0022_auto_20220209_0454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qc_report',
            name='color',
            field=models.CharField(blank=True, choices=[('SELECT', '请选择'), ('ONE_C', '单色'), ('ALL_C', '齐色')], default='SELECT', max_length=100, verbose_name='颜色'),
        ),
        migrations.AlterField(
            model_name='qc_report',
            name='product_status',
            field=models.CharField(blank=True, choices=[('SELECT', '请选择'), ('NEW_P', '刚出成品'), ('FINISH_P', '成品全部完成'), ('SEND_P', '大货包装完成')], default='SELECT', max_length=100, verbose_name='大货状态'),
        ),
    ]
