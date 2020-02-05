from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import (User, Factory,
                     Merchandiser, Designer, Shipping, Finance,
                     Qc, Office, Admin, Merchandiser_Manager, Post, PostAttachment,
                     Sample, Sample_size_specs, Sample_os_avatar,
                     Sample_os_pics, Sample_swatches,
                     Sample_pics_factory, Sample_quotation_form,
                     Sample_size_spec_factory)
from django.db import transaction
from tempus_dominus.widgets import DatePicker
from django.utils.translation import ugettext_lazy as _


class MyAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _("用户名和密码不匹配，请重新输入!"),
        'inactive': _("该账号已被冻结!"),
    }


USER_ROLE_TYPE = [
    (1, '工厂'),
    (2, '跟单'),
    (3, '设计师'),
    (4, '财务'),
    (5, '船务'),
    (6, '质检'),
    (7, '行政'),
    (8, '管理员'),
    (9, '跟单主管'),
]


class SignUpForm(UserCreationForm):
    username = forms.CharField(label=_('用户名'), error_messages={'required': "此字段必须填写！"})
    password1 = forms.CharField(label=_('密码'), error_messages={'required': "此字段必须填写！"})
    password2 = forms.CharField(label=_('确认密码'), error_messages={'required': "此字段必须填写！"})
    roles = forms.MultipleChoiceField(
        label=_('用户角色'),
        error_messages={'required': "必须选择一个以上用户角色！"},
        widget=forms.CheckboxSelectMultiple,
        choices=USER_ROLE_TYPE,
        required=True,
    )
    error_messages = {
        'password_mismatch': _("两次输入的密码不一致，请重新输入."),
    }

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'roles')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        roles = self.cleaned_data['roles']
        roles = list(map(int, roles))
        if 1 in roles:
            user.is_factory = True
        if 2 in roles:
            user.is_merchandiser = True
        if 3 in roles:
            user.is_designer = True
        if 4 in roles:
            user.is_finance = True
        if 5 in roles:
            user.is_shipping = True
        if 6 in roles:
            user.is_qc = True
        if 7 in roles:
            user.is_office = True
        if 8 in roles:
            user.is_admin = True
        if 9 in roles:
            user.is_merchandiser_manager = True
        user.save()
        if 1 in roles:
            Factory.objects.create(user=user)
        if 2 in roles:
            Merchandiser.objects.create(user=user)
        if 3 in roles:
            Designer.objects.create(user=user)
        if 4 in roles:
            Finance.objects.create(user=user)
        if 5 in roles:
            Shipping.objects.create(user=user)
        if 6 in roles:
            Qc.objects.create(user=user)
        if 7 in roles:
            Office.objects.create(user=user)
        if 8 in roles:
            Admin.objects.create(user=user)
        if 9 in roles:
            Merchandiser_Manager.objects.create(user=user)
        return user


class NewpostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'created_by', 'catagory')


class PostAttachmentForm(forms.ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('file',)


class NewsampleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsampleForm, self).__init__(*args, **kwargs)
        self.fields['brand'].empty_label = '请选择'
        self.fields['merchandiser'].empty_label = '请选择'
        self.fields['designer'].empty_label = '请选择'

    class Meta:
        model = Sample
        fields = ('has_os_sample', 'sample_no', 'brand',
                  'merchandiser', 'designer')
        error_messages = {
            'sample_no': {
                'required': "必填字段！",
            },
            'brand': {
                'required': "必填字段！",
            },
            'merchandiser': {
                'required': "必填字段！",
            },
            'designer': {
                'required': "必填字段！",
            },
        }


class SampleForm(forms.ModelForm):
    parcel_date = forms.DateField(widget=DatePicker(), label="寄件日期", required=False)
    qutation = forms.DecimalField(label="工厂报价(元)", required=False)

    def __init__(self, *args, **kwargs):
        super(SampleForm, self).__init__(*args, **kwargs)
        self.fields['brand'].empty_label = '请选择'
        self.fields['merchandiser'].empty_label = '请选择'
        self.fields['designer'].empty_label = '请选择'
        self.fields['factory'].empty_label = '请选择'
        self.fields['style'].empty_label = '请选择'

    class Meta:
        model = Sample
        fields = ('has_os_sample', 'sample_no', 'brand',
                  'merchandiser', 'designer', 'factory', 'style', 'qutation',
                  'parcel_date', 'alteration')
        widgets = {
                  'alteration': forms.Textarea(attrs={'rows': 6}),
                  }


class SampledetailForm(forms.ModelForm):
    parcel_date = forms.DateField(widget=DatePicker(), label="寄件日期", required=False)
    qutation = forms.DecimalField(label="工厂报价(元)", required=False)

    def __init__(self, *args, **kwargs):
        super(SampledetailForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['has_os_sample'].disabled = True
            self.fields['sample_no'].disabled = True
            self.fields['brand'].disabled = True
            self.fields['merchandiser'].disabled = True
            self.fields['designer'].disabled = True
            self.fields['factory'].disabled = True
            self.fields['style'].disabled = True
            self.fields['parcel_date'].disabled = True
            self.fields['alteration'].disabled = True

        def clean_has_os_sample_field(self):
            instance = getattr(self, 'instance', None)
            if instance and instance.id:
                return instance.has_os_sample
            else:
                return self.cleaned_data['has_os_sample']

        def clean_sample_no_field(self):
            instance = getattr(self, 'instance', None)
            if instance and instance.id:
                return instance.sample_no
            else:
                return self.cleaned_data['sample_no']

        def clean_brand_field(self):
            instance = getattr(self, 'instance', None)
            if instance and instance.id:
                return instance.brand
            else:
                return self.cleaned_data['brand']

        def clean_merchandiser_field(self):
            instance = getattr(self, 'instance', None)
            if instance and instance.id:
                return instance.merchandiser
            else:
                return self.cleaned_data['merchandiser']

        def clean_designer_field(self):
            instance = getattr(self, 'instance', None)
            if instance and instance.id:
                return instance.designer
            else:
                return self.cleaned_data['designer']

        def clean_factory_field(self):
            instance = getattr(self, 'instance', None)
            if instance and instance.id:
                return instance.factory
            else:
                return self.cleaned_data['factory']

        def clean_style_field(self):
            instance = getattr(self, 'instance', None)
            if instance and instance.id:
                return instance.style
            else:
                return self.cleaned_data['style']

        def clean_parcel_date_field(self):
            instance = getattr(self, 'instance', None)
            if instance and instance.id:
                return instance.parcel_date
            else:
                return self.cleaned_data['parcel_date']

        def clean_alteration_field(self):
            instance = getattr(self, 'instance', None)
            if instance and instance.id:
                return instance.alteration
            else:
                return self.cleaned_data['alteration']

    class Meta:
        model = Sample
        fields = ('has_os_sample', 'sample_no', 'brand',
                  'merchandiser', 'designer', 'factory', 'style', 'qutation',
                  'parcel_date', 'alteration')
        widgets = {
                  'alteration': forms.Textarea(attrs={'rows': 6}),
                  }


class SamplesizespecsForm(forms.ModelForm):
    class Meta:
        model = Sample_size_specs
        fields = ('file',)


class SampleswatchForm(forms.ModelForm):
    class Meta:
        model = Sample_swatches
        fields = ('file',)


class SamplefpicsForm(forms.ModelForm):
    class Meta:
        model = Sample_pics_factory
        fields = ('file',)


class SampleosavatarForm(forms.ModelForm):
    class Meta:
        model = Sample_os_avatar
        fields = ('file',)


class SamplequotationForm(forms.ModelForm):
    class Meta:
        model = Sample_quotation_form
        fields = ('file',)


class SamplesizespecfForm(forms.ModelForm):
    class Meta:
        model = Sample_size_spec_factory
        fields = ('file',)


class SampleospicsForm(forms.ModelForm):
    class Meta:
        model = Sample_os_pics
        fields = ('file',)
