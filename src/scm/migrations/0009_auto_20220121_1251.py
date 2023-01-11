# Generated by Django 3.0.7 on 2022-01-21 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0008_check_record_check_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check_record',
            name='grade',
            field=models.CharField(blank=True, choices=[(None, '请选择'), ('YZ', '严重'), ('CY', '次要')], max_length=50, verbose_name='严重等级'),
        ),
    ]
