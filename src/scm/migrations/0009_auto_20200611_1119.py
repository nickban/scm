# Generated by Django 3.0.7 on 2020-06-11 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0008_auto_20200611_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='PHangingtape',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scm.PHangingtape', verbose_name='挂衣绳'),
        ),
    ]
