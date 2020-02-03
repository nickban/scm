from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
import os
from django.utils.safestring import mark_safe
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
    created_date = models.DateTimeField('创建日期', auto_now_add=True)
    sample_no = models.CharField('样板号', max_length=100)
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
                                 verbose_name='买手',
                                 on_delete=models.CASCADE,
                                 related_name='samples')
    style = models.ForeignKey(Style,
                              verbose_name='款式',
                              on_delete=models.CASCADE,
                              related_name='samples',
                              null=True, blank=True)
    factory = models.ForeignKey(Factory,
                                verbose_name='工厂',
                                on_delete=models.CASCADE,
                                related_name='samples',
                                null=True, blank=True)
    parcel_date = models.DateField('寄件日期', null=True, blank=True)
    qutation = models.DecimalField('工厂报价',
                                   max_digits=5,
                                   decimal_places=2,
                                   null=True, blank=True)
    alteration = models.TextField('做板评语', blank=True)
    status = models.CharField('样板状态',
                              max_length=50,
                              choices=SAMPLE_STATUS,
                              blank=True,
                              default=NEW)


class Sample_size_spec_factory(models.Model):
    file = models.FileField(upload_to='sample/sample_size_spec_factory/', blank=True)
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE,
                                  related_name='sizespecf')


@receiver(models.signals.post_delete, sender=Sample_size_spec_factory)
def auto_delete_file_sample_size_spec_factory(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


class Sample_swatches(models.Model):
    img = models.ImageField(upload_to='sample/sample_swatches/', blank=True)
    sample = models.ForeignKey(Sample,
                               on_delete=models.CASCADE,
                               related_name='swatches')


@receiver(models.signals.post_delete, sender=Sample_swatches)
def auto_delete_file_sample_swatches(sender, instance, **kwargs):
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)


class Sample_os_avatar(models.Model):
    img = models.ImageField(upload_to='sample/sample_os_avatar/', blank=True)
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, primary_key=True,
                                  related_name='os_avatar')


@receiver(models.signals.post_delete, sender=Sample_os_avatar)
def auto_delete_file_sample_os_avatar(sender, instance, **kwargs):
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)


class Sample_quotation_form(models.Model):
    file = models.FileField(upload_to='sample/sample_quotation_form/', blank=True)
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, related_name='quotation')


@receiver(models.signals.post_delete, sender=Sample_quotation_form)
def auto_delete_file_sample_qutation_form(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


class Sample_os_pics(models.Model):
    img = models.ImageField(upload_to='sample/sample_os_pics/', blank=True)
    sample = models.ForeignKey(Sample,
                               on_delete=models.CASCADE,
                               related_name='os_pics')


@receiver(models.signals.post_delete, sender=Sample_os_pics)
def auto_delete_file_sample_os_pics(sender, instance, **kwargs):
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)


class Sample_pics_factory(models.Model):
    img = models.ImageField(upload_to='sample/sample_pics_factory/', blank=True)
    sample = models.ForeignKey(Sample,
                               on_delete=models.CASCADE,
                               related_name='factory_pics')


@receiver(models.signals.post_delete, sender=Sample_pics_factory)
def auto_delete_file_sample_pics_factory(sender, instance, **kwargs):
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)


class Sample_size_specs(models.Model):
    file = models.FileField(upload_to='sample/sample_size_specs/', blank=True)
    sample = models.ForeignKey(Sample,
                               on_delete=models.CASCADE,
                               related_name='size_specs')


@receiver(models.signals.post_delete, sender=Sample_size_specs)
def auto_delete_file_sample_size_specs(sender, instance, **kwargs):
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
