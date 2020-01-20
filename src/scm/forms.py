from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _

class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("用户名"), 
                               max_length=254)
    password = forms.CharField(label=_("密码"), 
                               widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': _("用户名和密码不匹配，请重新输入!"),
        'inactive': _("该账号已被冻结!"),
    }
