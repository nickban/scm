# Generated by Django 3.0.7 on 2022-01-22 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0011_auto_20220122_0410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qc_report',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qcreports', to='scm.Order'),
        ),
    ]