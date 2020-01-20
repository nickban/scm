from django.db import models
from django.contrib.auth.models import AbstractUser
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


class Sample(models.Model):
    NEW = 'NEW'
    COMPLETED = 'COMPLETED'
    SAMPLE_STATUS = [
        (NEW, 'NEW'),
        (COMPLETED, 'COMPLETED'),
    ]
    os_avatar = models.ImageField('原版头像',
                                  upload_to='samples/avatar/',
                                  blank=True)
    created_date = models.DateTimeField('创建日期', auto_now=True)
    created_by = models.ForeignKey(User,
                                   verbose_name='创建人',
                                   on_delete=models.CASCADE,
                                   related_name='samples')
    sample_no = models.PositiveIntegerField('样板号')
    has_os_sample = models.BooleanField('是否有原版', )
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
                              related_name='samples')
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
    os_pic = models.ImageField('原版照片',
                               upload_to='samples/os_pics/',
                               blank=True)
    sample_pic = models.ImageField('样板照片',
                                   upload_to='samples/pics/',
                                   blank=True)
    swatch_pic = models.ImageField('色卡',
                                   upload_to='samples/swatch/',
                                   blank=True)
    alteration = models.TextField('制版评语', blank=True)
    size_spec = models.FileField('评语附件',
                                 upload_to='samples/size_spec/',
                                 blank=True)
    size_spec_factory = models.ImageField('样板尺寸表',
                                          upload_to='samples/size_spec_factory/',
                                          blank=True)
    status = models.CharField('样板状态',
                              max_length=50,
                              choices=SAMPLE_STATUS,
                              blank=True)


class Order(models.Model):
    pass
