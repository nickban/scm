# Generated by Django 3.0.2 on 2020-01-31 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0002_auto_20200131_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='sample_no',
            field=models.CharField(error_messages={'required': '必填字段！'}, max_length=100, verbose_name='样板号'),
        ),
    ]
