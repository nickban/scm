from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
import os
# Create your models here.


class User(AbstractUser):
    is_factory = models.BooleanField(default=False)
    is_merchandiser = models.BooleanField(default=False)
    is_designer = models.BooleanField(default=False)
    is_finance = models.BooleanField(default=False)
    is_shipping = models.BooleanField(default=False)
    is_qc = models.BooleanField(default=False)
    is_office = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_merchandiser_manager = models.BooleanField(default=False)


class Factory(models.Model):
    user = models.OneToOneField(User, verbose_name='工厂',
                                on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Merchandiser(models.Model):
    user = models.OneToOneField(User, verbose_name='跟单',
                                on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Designer(models.Model):
    user = models.OneToOneField(User, verbose_name='设计师',
                                on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Finance(models.Model):
    user = models.OneToOneField(User, verbose_name='财务',
                                on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Shipping(models.Model):
    user = models.OneToOneField(User, verbose_name='船务',
                                on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Qc(models.Model):
    user = models.OneToOneField(User, verbose_name='质检',
                                on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Admin(models.Model):
    user = models.OneToOneField(User, verbose_name='管理员',
                                on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Office(models.Model):
    user = models.OneToOneField(User, verbose_name='行政',
                                on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Merchandiser_Manager(models.Model):
    user = models.OneToOneField(User, verbose_name='跟单主管',
                                on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Style(models.Model):
    name = models.CharField('款式', max_length=50)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField('品牌', max_length=50)

    def __str__(self):
        return self.name

# 色卡部分定义


class Fabric_Shop(models.Model):
    name = models.CharField('档口名', max_length=100)


class Fabric_Item(models.Model):
    name = models.CharField('品名', max_length=100)
    fabric_shop = models.ForeignKey(Fabric_Shop,
                                    on_delete=models.CASCADE,
                                    related_name='fabricitems')


class Swatch(models.Model):
    fabric_item = models.ForeignKey(Fabric_Item,
                                    on_delete=models.CASCADE,
                                    related_name='swatches')
    pic = models.ImageField(upload_to='swatches/', blank=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name='swatches')

# 样板部分模块定义


class Sample(models.Model):
    NEW = 'NEW'
    SENT_FACTORY = 'SENT_F'
    COMPLETED = 'COMPLETED'
    SAMPLE_STATUS = [
        (NEW, '新建'),
        (SENT_FACTORY, '送工厂'),
        (COMPLETED, '完成'),
    ]
    os_avatar = models.ImageField('款式图',
                                  upload_to='samples/avatar/',
                                  blank=True)
    created_date = models.DateTimeField('创建日期', auto_now=True)
    sample_no = models.PositiveIntegerField('样板号')
    has_os_sample = models.BooleanField('是否有原版?', )
    brand = models.ForeignKey(Brand,
                              verbose_name='品牌',
                              on_delete=models.CASCADE,
                              related_name='samples')
    merchandiser = models.ForeignKey(Merchandiser,
                                     verbose_name='跟单',
                                     on_delete=models.CASCADE,
                                     related_name='samples')
    designer = models.ForeignKey(Designer,
                                 verbose_name='设计师',
                                 on_delete=models.CASCADE,
                                 related_name='samples')
    style = models.ForeignKey(Style,
                              verbose_name='款式',
                              on_delete=models.CASCADE,
                              related_name='samples',
                              null=True)
    factory = models.ForeignKey(Factory,
                                verbose_name='工厂',
                                on_delete=models.CASCADE,
                                related_name='samples')
    parcel_date = models.DateField('寄件日期', null=True, blank=True)
    qutation = models.DecimalField('工厂报价',
                                   max_digits=5,
                                   decimal_places=2,
                                   null=True, blank=True)
    qutation_form = models.ImageField('报价单',
                                      upload_to='samples/qutation/',
                                      blank=True)
    alteration = models.TextField('做板评语', blank=True)
    swatches = models.ManyToManyField(Swatch, null=True, blank=True)
    size_spec_factory = models.ImageField('尺寸表(工厂)',
                                          upload_to='samples/size_spec_factory/',
                                          blank=True)
    status = models.CharField('样板状态',
                              max_length=50,
                              choices=SAMPLE_STATUS,
                              blank=True)


class Sample_os_pics(models.Model):
    img = models.ImageField(upload_to='samples/os_pics/', blank=True)
    sample = models.ForeignKey(Sample,
                               on_delete=models.CASCADE,
                               verbose_name='样板',
                               related_name='os_pics')


@receiver(models.signals.post_delete, sender=Sample_os_pics)
def auto_delete_file_sampleospics(sender, instance, **kwargs):
    if instance.os_pic:
        if os.path.isfile(instance.os_pic.path):
            os.remove(instance.os_pic.path)


class Sample_pics(models.Model):
    pic = models.ImageField(upload_to='samples/pics/', blank=True)
    sample = models.ForeignKey(Sample,
                               on_delete=models.CASCADE,
                               verbose_name='样板',
                               related_name='pics')


@receiver(models.signals.post_delete, sender=Sample_pics)
def auto_delete_file_samplepics(sender, instance, **kwargs):
    if instance.pic:
        if os.path.isfile(instance.pic.path):
            os.remove(instance.pic.path)


class Sample_size_specs(models.Model):
    file = models.FileField(upload_to='samples/size_specs/', blank=True)
    sample = models.ForeignKey(Sample,
                               on_delete=models.CASCADE,
                               verbose_name='样板',
                               related_name='size_specs')


@receiver(models.signals.post_delete, sender=Sample_size_specs)
def auto_delete_file_sizespecs(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

# 信息部分定义


N = '通知'
M = '手册'
NOTIFICATION_CATAGORY = [
    (N, '通知'),
    (M, '手册'),
]


class Post(models.Model):
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    create_time = models.DateField('发布日期', auto_now_add=True)
    created_by = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name='发布人')
    catagory = models.CharField('类别', max_length=100, choices=NOTIFICATION_CATAGORY)

    def get_absolute_url(self):
        return reverse('post:postedit', args=[str(self.id)])


class PostAttachment(models.Model):
    file = models.FileField(upload_to='post/', blank=True)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             verbose_name='关联信息',
                             related_name='postattachments')


@receiver(models.signals.post_delete, sender=PostAttachment)
def auto_delete_file_postattachment(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


class Order(models.Model):
    pass
