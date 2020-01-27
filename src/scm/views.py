from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView, DeleteView
from .models import User, Post
from .forms import SignUpForm, NewpostForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import reverse_lazy
from .decorators import office_required


@method_decorator([login_required], name='dispatch')
class home(TemplateView):
    template_name = 'home.html'


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


@method_decorator([login_required], name='dispatch')
class PostList(ListView):
    model = Post
    ordering = ('create_time', )
    context_object_name = 'posts'
    template_name = 'post_list.html'


@method_decorator([login_required, office_required], name='dispatch')
class PostAdd(CreateView):
    model = Post
    form_class = NewpostForm
    template_name = 'post_add.html'

    def form_valid(self, form):
        form.save()
        return redirect('post:postlist')


@method_decorator([login_required, office_required], name='dispatch')
class PostEdit(UpdateView):
    model = Post
    fields = ['title', 'content', 'created_by', 'catagory', 'attachment']
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post:postlist')


@method_decorator([login_required], name='dispatch')
class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'


@method_decorator([login_required, office_required], name='dispatch')
class PostDelete(DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post:postlist')
