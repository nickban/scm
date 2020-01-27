# Generated by Django 3.0.2 on 2020-01-27 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0006_auto_20200123_0645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='attachment',
        ),
        migrations.CreateModel(
            name='PostAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='post/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postattachments', to='scm.Post', verbose_name='关联信息')),
            ],
        ),
    ]
