from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import (TemplateView,
                                  CreateView, ListView, UpdateView, DetailView,
                                  DeleteView)
from .models import User, Post, PostAttachment
from .forms import SignUpForm, NewpostForm, PostAttachmentForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import reverse_lazy
from .decorators import office_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views import View
from django.db import transaction


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


def postattach(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                attach = form.save(commit=False)
                attach.post = post
                attach.save()
                data = {"files": [{
                        "name": attach.file.name,
                        "url": attach.file.url, },
                        ]}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return render(request, 'post_attach.html', {'post': post})


@method_decorator([login_required, office_required], name='dispatch')
class PostEdit(UpdateView):
    model = Post
    fields = ['title', 'content', 'created_by', 'catagory']
    template_name = 'post_edit.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post:postlist')

    def get_context_data(self, **kwargs):
        kwargs['attachments'] = self.get_object().postattachments.all()
        return super().get_context_data(**kwargs)


@method_decorator([login_required], name='dispatch')
class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['attachments'] = self.get_object().postattachments.all()
        return super().get_context_data(**kwargs)


@method_decorator([login_required, office_required], name='dispatch')
class PostDelete(DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post:postlist')


@method_decorator([login_required, office_required], name='dispatch')
class PostAttachDelete(DeleteView):
    model = PostAttachment
    pk_url_kwarg = 'postattach_pk'
    context_object_name = 'postattach'
    template_name = 'post_attach_delete.html'

    def get_success_url(self):
        post = self.object.post
        return reverse_lazy('post:postedit', kwargs={'pk': post.pk})
