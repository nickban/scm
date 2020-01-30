from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import (TemplateView,
                                  CreateView, ListView, UpdateView, DetailView,
                                  DeleteView)
from .models import User, Post, PostAttachment, Sample, Sample_os_pics, Sample_size_specs, Sample_pics
from .forms import (SignUpForm, NewpostForm, PostAttachmentForm,
                    NewsampleForm, SampleForm, SamplesizespecsForm)
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import reverse_lazy
from .decorators import office_required, merchandiser_required
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

# 样板部分试图定义


@method_decorator([login_required], name='dispatch')
class SampleList(ListView):
    model = Sample
    ordering = ('created_date', )
    context_object_name = 'samples'
    template_name = 'sample_list.html'
    paginate_by = 10
    queryset = Sample.objects.all()


@method_decorator([login_required], name='dispatch')
class SampleAdd(CreateView):
    model = Sample
    form_class = NewsampleForm
    template_name = 'sample_add.html'
    success_url = reverse_lazy('sample:samplelist')


@method_decorator([login_required], name='dispatch')
class SampleEdit(UpdateView):
    model = Sample
    form_class = SampleForm
    template_name = 'sampleedit.html'
    context_object_name = 'sample'
    success_url = reverse_lazy('sample:samplelist')

    def get_context_data(self, **kwargs):
        kwargs['os_pics'] = self.get_object().os_pics.all()
        kwargs['pics'] = self.get_object().pics.all()
        kwargs['size_specs'] = self.get_object().size_specs.all()
        return super().get_context_data(**kwargs)


@method_decorator([login_required], name='dispatch')
class SampleospicDelete(DeleteView):
    model = Sample_os_pics
    pk_url_kwarg = 'sample_ospic_pk'
    context_object_name = 'sampleospic'
    template_name = 'sample_ospic_delete.html'

    def get_success_url(self):
        sample = self.object.sample
        return reverse_lazy('sample:sampleedit', kwargs={'pk': sample.pk})


@method_decorator([login_required], name='dispatch')
class SamplesizespecDelete(DeleteView):
    model = Sample_size_specs
    pk_url_kwarg = 'sample_sizespec_pk'
    context_object_name = 'samplesizespec'
    template_name = 'sample_sizespec_delete.html'

    def get_success_url(self):
        sample = self.object.sample
        return reverse_lazy('sample:sampleedit', kwargs={'pk': sample.pk})


@method_decorator([login_required], name='dispatch')
class SamplepicDelete(DeleteView):
    model = Sample_pics
    pk_url_kwarg = 'sample_pic_pk'
    context_object_name = 'samplepic'
    template_name = 'sample_pic_delete.html'

    def get_success_url(self):
        sample = self.object.sample
        return reverse_lazy('sample:sampleedit', kwargs={'pk': sample.pk})


@login_required
def samplesizespecadd(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    if request.method == 'POST':
        form = SamplesizespecsForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                sizespec = form.save(commit=False)
                sizespec.sample = sample
                sizespec.save()
                data = {"files": [{
                        "name": sizespec.file.name,
                        "url": sizespec.file.url, },
                        ]}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return render(request, 'sample_size_spec_add.html', {'sample': sample})


class SampleDetail(TemplateView):
    template_name = 'sample_list.html'


class SampleDelete(TemplateView):
    template_name = 'sample_list.html'

# 订单部分试图


class OrderList(TemplateView):
    template_name = 'order_list.html'


class FunctionList(TemplateView):
    template_name = 'function_list.html'


class InvoiceList(TemplateView):
    template_name = 'invoice_list.html'

# Post 部分试图定义


@method_decorator([login_required], name='dispatch')
class PostList(ListView):
    model = Post
    ordering = ('create_time', )
    context_object_name = 'posts'
    template_name = 'post_list.html'
    paginate_by = 10
    queryset = Post.objects.all()


@method_decorator([login_required, office_required], name='dispatch')
class PostAdd(CreateView):
    model = Post
    form_class = NewpostForm
    template_name = 'post_add.html'


@login_required
@office_required
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
