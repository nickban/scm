from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from .models import User
from .forms import SignUpForm
from django.contrib.auth import login


def home(request):
    user = request.user
    if user.is_authenticated:
        if user.is_factory or \
                user.is_merchandiser or \
                user.is_designer or \
                user.is_office or \
                user.is_merchandiser_manager:
            return redirect('sample:sample_list')
        elif user.is_qc or \
                user.is_shipping:
            return redirect('order:order_list')
        elif user.is_admin:
            return redirect('admin:function_list')
        else:
            return redirect('finance:invoice_list')
    return redirect('login')


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')


class SampleList(TemplateView):
    template_name = 'sample_list.html'


class OrderList(TemplateView):
    template_name = 'order_list.html'


class FunctionList(TemplateView):
    template_name = 'function_list.html'


class InvoiceList(TemplateView):
    template_name = 'invoice_list.html'
