# Generated by Django 3.0.2 on 2020-02-05 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0007_auto_20200203_0418'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sample_os_avatar',
            old_name='img',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='sample_os_pics',
            old_name='img',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='sample_pics_factory',
            old_name='img',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='sample_swatches',
            old_name='img',
            new_name='file',
        ),
    ]
