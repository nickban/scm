# Generated by Django 3.0.2 on 2020-01-30 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='designer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='scm.Designer', verbose_name='买手'),
        ),
    ]
