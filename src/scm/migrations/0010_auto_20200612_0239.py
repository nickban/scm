# Generated by Django 3.0.7 on 2020-06-12 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0009_auto_20200611_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='PHangingtape',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='挂衣绳'),
        ),
        migrations.DeleteModel(
            name='PHangingtape',
        ),
    ]
