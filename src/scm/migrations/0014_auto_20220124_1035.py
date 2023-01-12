# Generated by Django 3.0.7 on 2022-01-24 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0013_check_record_pics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check_record',
            name='file',
        ),
        migrations.AddField(
            model_name='check_record',
            name='comments',
            field=models.CharField(max_length=500, null=True, verbose_name='QC备注'),
        ),
        migrations.AlterField(
            model_name='check_point',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='描述'),
        ),
    ]