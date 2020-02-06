# Generated by Django 3.0.2 on 2020-02-05 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0008_auto_20200205_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample_os_avatar',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sample_os_avatar',
            name='sample',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='os_avatar', to='scm.Sample'),
        ),
    ]
