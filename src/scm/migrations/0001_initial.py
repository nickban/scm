# Generated by Django 3.0.2 on 2020-01-30 12:39

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_factory', models.BooleanField(default=False)),
                ('is_merchandiser', models.BooleanField(default=False)),
                ('is_designer', models.BooleanField(default=False)),
                ('is_finance', models.BooleanField(default=False)),
                ('is_shipping', models.BooleanField(default=False)),
                ('is_qc', models.BooleanField(default=False)),
                ('is_office', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_merchandiser_manager', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='品牌')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='发布日期')),
                ('catagory', models.CharField(choices=[('通知', '通知'), ('手册', '手册')], max_length=100, verbose_name='类别')),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True, verbose_name='创建日期')),
                ('sample_no', models.PositiveIntegerField(verbose_name='样板号')),
                ('has_os_sample', models.BooleanField(verbose_name='是否有原版?')),
                ('parcel_date', models.DateField(blank=True, null=True, verbose_name='寄件日期')),
                ('qutation', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='工厂报价')),
                ('alteration', models.TextField(blank=True, verbose_name='做板评语')),
                ('status', models.CharField(blank=True, choices=[('NEW', '新建'), ('SENT_F', '送工厂'), ('COMPLETED', '完成')], max_length=50, verbose_name='样板状态')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='scm.Brand', verbose_name='品牌')),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='款式')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='管理员')),
            ],
        ),
        migrations.CreateModel(
            name='Designer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='设计师')),
            ],
        ),
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='工厂')),
            ],
        ),
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='财务')),
            ],
        ),
        migrations.CreateModel(
            name='Merchandiser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='跟单')),
            ],
        ),
        migrations.CreateModel(
            name='Merchandiser_Manager',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='跟单主管')),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='行政')),
            ],
        ),
        migrations.CreateModel(
            name='Qc',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='质检')),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='船务')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_swatches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(blank=True, upload_to='sample/sample_swatches/')),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_size_specs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='sample/sample_size_specs/')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size_specs', to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_size_spec_factory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='sample/sample_size_spec_factory/')),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_qutation_form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='sample/sample_qutation_form/')),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_pics_factory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(blank=True, upload_to='sample/sample_pics_factory/')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pics_factory', to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_os_pics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, upload_to='sample/sample_os_pics/')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='os_pics', to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_os_avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, upload_to='sample/sample_os_avatar/')),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scm.Sample')),
            ],
        ),
        migrations.AddField(
            model_name='sample',
            name='style',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='scm.Style', verbose_name='款式'),
        ),
        migrations.CreateModel(
            name='PostAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='post/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postattachments', to='scm.Post', verbose_name='关联信息')),
            ],
        ),
        migrations.AddField(
            model_name='sample',
            name='designer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='scm.Designer', verbose_name='买手'),
        ),
        migrations.AddField(
            model_name='sample',
            name='factory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='scm.Factory', verbose_name='工厂'),
        ),
        migrations.AddField(
            model_name='sample',
            name='merchandiser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='scm.Merchandiser', verbose_name='跟单'),
        ),
        migrations.AddField(
            model_name='post',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm.Office', verbose_name='发布人'),
        ),
    ]
