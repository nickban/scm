# Generated by Django 3.0.7 on 2022-03-01 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scm', '0028_auto_20220209_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_production',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('production', models.CharField(max_length=200, verbose_name='大货进度')),
                ('status', models.CharField(choices=[('NORMAL', '正常'), ('WARNING', '警告')], default='NORMAL', max_length=100, verbose_name='状态')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productions', to='scm.Order')),
            ],
        ),
    ]
