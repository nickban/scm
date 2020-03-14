# Generated by Django 3.0.4 on 2020-03-14 03:17

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
            name='Additiontag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='附加挂牌编号')),
                ('file', models.FileField(blank=True, upload_to='order/additiontag/', verbose_name='图片')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='品牌')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('invoice_no', models.CharField(max_length=100, verbose_name='发票号')),
                ('status', models.CharField(choices=[('NEW', '新建'), ('CONFIRMED', '财务已确认'), ('PAID', '已付款')], default='NEW', max_length=50, verbose_name='状态')),
                ('file', models.FileField(blank=True, upload_to='order/invoice/')),
                ('handoverdate', models.DateTimeField(null=True, verbose_name='出货日期')),
                ('start_of_week', models.DateTimeField(null=True)),
                ('end_of_week', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mainlabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='主唛编号')),
                ('file', models.FileField(blank=True, upload_to='order/mainlabel/', verbose_name='图片')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mainlabels', to='scm.Brand', verbose_name='品牌')),
            ],
        ),
        migrations.CreateModel(
            name='Maintag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='挂牌编号')),
                ('file', models.FileField(blank=True, upload_to='order/maintag/', verbose_name='图片')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintags', to='scm.Brand', verbose_name='品牌')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('status', models.CharField(blank=True, choices=[('NEW', '新建'), ('SENT_FACTORY', '送工厂'), ('CONFIRMED', '已确认'), ('SHIPPED', '已出货')], default='NEW', max_length=50, verbose_name='订单状态')),
                ('po', models.CharField(max_length=100, verbose_name='订单号')),
                ('style_no', models.CharField(max_length=100, verbose_name='款号')),
                ('order_type', models.CharField(blank=True, choices=[(None, '请选择'), ('NEWORDER', '新单'), ('REPEATORDER', '翻单')], max_length=50, verbose_name='订单类型')),
                ('destination', models.CharField(blank=True, choices=[(None, '请选择'), ('AU', '澳洲'), ('NZ', '新西兰'), ('SG', '新加坡')], max_length=50, verbose_name='目的地')),
                ('childorder', models.CharField(blank=True, choices=[(None, '请选择'), ('CNZ', 'NZ'), ('CSG', 'SG'), ('CNZSG', 'NZ,SG')], max_length=50, verbose_name='小单')),
                ('tran_type', models.CharField(blank=True, choices=[(None, '请选择'), ('SEA', '海运'), ('AIR', '空运')], max_length=50, verbose_name='运输类型')),
                ('factory_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='工厂价格')),
                ('disigner_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='客人价格')),
                ('handover_date_f', models.DateField(blank=True, null=True, verbose_name='工厂交期')),
                ('handover_date_d', models.DateField(blank=True, null=True, verbose_name='客人交期')),
                ('comments', models.TextField(blank=True, verbose_name='大货要求')),
                ('labeltype', models.CharField(blank=True, choices=[(None, '请选择'), ('NUMBER', '数字码'), ('ALPHABET', '字母码')], default='NUMBER', max_length=50, verbose_name='码标类型')),
                ('addition_tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scm.Additiontag', verbose_name='附加挂牌')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='scm.Brand', verbose_name='品牌')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='scm.Invoice', verbose_name='发票号')),
                ('main_label', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scm.Mainlabel', verbose_name='主唛')),
                ('main_tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scm.Maintag', verbose_name='挂牌')),
            ],
        ),
        migrations.CreateModel(
            name='Order_color_ratio_qty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('color', models.CharField(max_length=100, verbose_name='颜色(英文)')),
                ('color_cn', models.CharField(max_length=100, verbose_name='颜色(中文)')),
                ('color_no', models.CharField(max_length=100, verbose_name='色号')),
                ('ratio', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='比列')),
                ('size1', models.PositiveSmallIntegerField()),
                ('size2', models.PositiveSmallIntegerField()),
                ('size3', models.PositiveSmallIntegerField()),
                ('size4', models.PositiveSmallIntegerField()),
                ('size5', models.PositiveSmallIntegerField()),
                ('bags', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('qty', models.PositiveSmallIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colorqtys', to='scm.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Packingtype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortname', models.CharField(max_length=50, verbose_name='包装方式')),
                ('description', models.TextField(blank=True, verbose_name='说明')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='发布日期')),
                ('catagory', models.CharField(choices=[('通知', '通知'), ('手册', '手册')], max_length=100, verbose_name='类别')),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('sample_no', models.CharField(max_length=100, verbose_name='样板号')),
                ('has_os_sample', models.BooleanField(verbose_name='是否有原版?')),
                ('parcel_date', models.DateField(blank=True, null=True, verbose_name='寄件日期')),
                ('qutation', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='工厂报价')),
                ('alteration', models.TextField(blank=True, verbose_name='做板评语')),
                ('status', models.CharField(blank=True, choices=[('NEW', '新建'), ('SENT_F', '送工厂'), ('COMPLETED', '完成')], default='NEW', max_length=50, verbose_name='样板状态')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='samples', to='scm.Brand', verbose_name='品牌')),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='款式')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='管理员')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Designer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='设计师')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='工厂')),
                ('show', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100, verbose_name='工厂名称')),
                ('contactperson', models.CharField(max_length=100, verbose_name='联系人')),
                ('address', models.CharField(max_length=200, verbose_name='地址')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=100, verbose_name='手机')),
                ('bank', models.CharField(max_length=100, null=True, verbose_name='开户银行')),
                ('bankaccount', models.CharField(max_length=100, null=True, verbose_name='银行账户')),
                ('bankaccountnumber', models.CharField(max_length=100, null=True, verbose_name='银行账号')),
            ],
        ),
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='财务')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Merchandiser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='跟单')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Merchandiser_Manager',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='跟单主管')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='行政')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Qc',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='质检')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='船务')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sample_swatches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(blank=True, upload_to='sample/swatches/')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='swatches', to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_size_specs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='sample/size_specs/')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size_specs', to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_size_spec_factory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='sample/size_spec_factory/')),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sizespecf', to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_quotation_form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='sample/quotation_form/')),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quotation', to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_pics_factory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(blank=True, upload_to='sample/pics_factory/')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factory_pics', to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_os_pics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(blank=True, upload_to='sample/os_pics/')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='os_pics', to='scm.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='Sample_os_avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(blank=True, upload_to='sample/os_avatar/')),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='os_avatar', to='scm.Sample')),
            ],
        ),
        migrations.AddField(
            model_name='sample',
            name='style',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='samples', to='scm.Style', verbose_name='款式'),
        ),
        migrations.CreateModel(
            name='PostAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='post/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postattachments', to='scm.Post', verbose_name='关联信息')),
            ],
        ),
        migrations.CreateModel(
            name='Order_swatches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='order/swatches/')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='swatches', to='scm.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Order_size_specs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='order/size_specs/')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sizespecs', to='scm.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Order_shipping_sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('shipping_sample', models.CharField(max_length=200, verbose_name='船头板进度')),
                ('status', models.CharField(choices=[('NORMAL', '正常'), ('WARNING', '警告')], default='NORMAL', max_length=100, verbose_name='状态')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shippingsamples', to='scm.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Order_shipping_pics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='order/shipping_pics/')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shippingpics', to='scm.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Order_packing_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NEW', '新建'), ('SUBMIT', '工厂已提交'), ('CLOSED', '已确认')], default='NEW', max_length=100, verbose_name='状态')),
                ('length', models.DecimalField(blank=True, decimal_places=2, default=54, max_digits=5, null=True, verbose_name='长')),
                ('width', models.DecimalField(blank=True, decimal_places=2, default=40, max_digits=5, null=True, verbose_name='宽')),
                ('height', models.DecimalField(blank=True, decimal_places=2, default=35, max_digits=5, null=True, verbose_name='高')),
                ('cube', models.DecimalField(blank=True, decimal_places=2, default=0.8, max_digits=5, null=True, verbose_name='体积')),
                ('gross_weight', models.DecimalField(blank=True, decimal_places=2, default=14, max_digits=5, null=True, verbose_name='毛重')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='packing_status', to='scm.Order', verbose_name='订单')),
            ],
        ),
        migrations.CreateModel(
            name='Order_packing_ctn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('ctn_start_no', models.PositiveSmallIntegerField()),
                ('ctn_end_no', models.PositiveSmallIntegerField()),
                ('totalboxes', models.PositiveSmallIntegerField()),
                ('sharebox', models.BooleanField(default=False)),
                ('bags', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('size1', models.PositiveSmallIntegerField()),
                ('size2', models.PositiveSmallIntegerField()),
                ('size3', models.PositiveSmallIntegerField()),
                ('size4', models.PositiveSmallIntegerField()),
                ('size5', models.PositiveSmallIntegerField()),
                ('totalqty', models.PositiveSmallIntegerField()),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packing_ctns', to='scm.Order_color_ratio_qty')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packing_ctns', to='scm.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Order_fitting_sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('sample', models.CharField(max_length=200, verbose_name='生产办进度')),
                ('status', models.CharField(choices=[('NORMAL', '正常'), ('WARNING', '警告')], default='NORMAL', max_length=100, verbose_name='状态')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fittingsamples', to='scm.Order')),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='Order_child_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('child_order', models.CharField(max_length=200, verbose_name='小单')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='childorders', to='scm.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Order_bulk_fabric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('bulk_fabric', models.CharField(max_length=200, verbose_name='大货布进度')),
                ('status', models.CharField(choices=[('NORMAL', '正常'), ('WARNING', '警告')], default='NORMAL', max_length=100, verbose_name='状态')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bulkfabrics', to='scm.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Barcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='order/barcodes/')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='barcode', to='scm.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Order_avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(blank=True, upload_to='order/avatar/')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='avatar', to='scm.Order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='packing_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scm.Packingtype', verbose_name='包装方式'),
        ),
        migrations.AddField(
            model_name='order',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suborders', to='scm.Order', verbose_name='父订单'),
        ),
        migrations.AddField(
            model_name='order',
            name='sample',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='scm.Sample', verbose_name='关联原板'),
        ),
        migrations.AddField(
            model_name='order',
            name='style',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='scm.Style', verbose_name='款式'),
        ),
        migrations.AddField(
            model_name='additiontag',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='additiontags', to='scm.Brand', verbose_name='品牌'),
        ),
        migrations.AddField(
            model_name='sample',
            name='designer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='samples', to='scm.Designer', verbose_name='买手'),
        ),
        migrations.AddField(
            model_name='sample',
            name='factory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='samples', to='scm.Factory', verbose_name='工厂'),
        ),
        migrations.AddField(
            model_name='sample',
            name='merchandiser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='samples', to='scm.Merchandiser', verbose_name='跟单'),
        ),
        migrations.AddField(
            model_name='post',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm.Office', verbose_name='发布人'),
        ),
        migrations.AddField(
            model_name='order',
            name='designer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='scm.Designer', verbose_name='买手'),
        ),
        migrations.AddField(
            model_name='order',
            name='factory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='scm.Factory', verbose_name='工厂'),
        ),
        migrations.AddField(
            model_name='order',
            name='merchandiser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='scm.Merchandiser', verbose_name='跟单'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='factory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='scm.Factory', verbose_name='工厂'),
        ),
    ]
