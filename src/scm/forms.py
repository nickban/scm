from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import (User, Factory,
                     Merchandiser, Designer, Shipping, Finance,
                     Qc, Office, Admin, Merchandiser_Manager, Post)
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import ClearableFileInput


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
