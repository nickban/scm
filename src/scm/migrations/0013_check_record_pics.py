# Generated by Django 3.0.7 on 2022-01-23 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0012_auto_20220122_2342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check_record_pics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='order/checkrecordpics/')),
                ('checkrecord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pics', to='scm.Check_record')),
            ],
        ),
    ]
