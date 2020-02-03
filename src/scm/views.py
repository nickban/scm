from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import (TemplateView,
                                  CreateView, ListView, UpdateView, DetailView,
                                  DeleteView)
from .models import (User, Post, PostAttachment, Sample, Sample_os_pics,
                     Sample_size_specs, Sample_os_avatar,
                     Sample_swatches, Sample_quotation_form,
                     Sample_pics_factory, Sample_size_spec_factory)
from .forms import (SignUpForm, NewpostForm, PostAttachmentForm,
                    NewsampleForm, SampleForm, SamplesizespecsForm,
                    SampleosavatarForm, SampleospicsForm,
                    SampleswatchForm, SamplefpicsForm, SampleoquotationForm,
                    SampleosizespecfForm)
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import reverse_lazy
from .decorators import office_required, merchandiser_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views import View
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


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
    ordering = ('-created_date', )
    context_object_name = 'samples'
    template_name = 'sample_list.html'
    paginate_by = 10
    queryset = Sample.objects.all()


@method_decorator([login_required], name='dispatch')
class SampleAddStep1(CreateView):
    model = Sample
    form_class = NewsampleForm
    template_name = 'sample_add.html'

    def form_valid(self, form):
        sample = form.save()
        return redirect('sample:sampleaddstep2', pk=sample.pk)


@method_decorator([login_required], name='dispatch')
class SampleAddStep2(UpdateView):
    model = Sample
    form_class = NewsampleForm
    template_name = 'sample_add.html'

    def form_valid(self, form):
        sample = form.save()
        return redirect('sample:sampleaddstep2', pk=sample.pk)

    def get_context_data(self, **kwargs):
        try:
            kwargs['os_avatar'] = self.get_object().os_avatar
        except ObjectDoesNotExist:
            kwargs['os_avatar'] = ''
        kwargs['os_pics'] = self.get_object().os_pics.all()
        kwargs['size_specs'] = self.get_object().size_specs.all()
        return super().get_context_data(**kwargs)


@method_decorator([login_required], name='dispatch')
class SampleEdit(UpdateView):
    model = Sample
    form_class = SampleForm
    template_name = 'sample_edit.html'
    context_object_name = 'sample'

    def get_context_data(self, **kwargs):
        kwargs['os_pics'] = self.get_object().os_pics.all()
        kwargs['size_specs'] = self.get_object().size_specs.all()
        kwargs['swatches'] = self.get_object().swatches.all()
        kwargs['fpics'] = self.get_object().factory_pics.all()
        try:
            kwargs['quotation'] = self.get_object().quotation
        except ObjectDoesNotExist:
            kwargs['quotation'] = ''
        try:
            kwargs['sizespecf'] = self.get_object().sizespecf
        except ObjectDoesNotExist:
            kwargs['sizespecf'] = ''
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        sample = form.save()
        return redirect('sample:sampleedit', pk=sample.pk)


# sample os pic view

@method_decorator([login_required], name='dispatch')
class SampleospicDelete(DeleteView):
    model = Sample_os_pics
    pk_url_kwarg = 'sample_ospic_pk'
    context_object_name = 'sampleospic'
    template_name = 'sample_ospic_delete.html'

    def get_success_url(self):
        sample = self.object.sample
        preurl = self.kwargs['preurl']
        print(preurl)
        return reverse_lazy('sample:sampleospicscollection', kwargs={'pk': sample.pk, 'preurl': preurl})


@login_required
def sampleospicadd(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    previous_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = SampleospicsForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                ospic = form.save(commit=False)
                ospic.sample = sample
                ospic.save()
                data = {"files": [{
                        "name": ospic.img.name,
                        "url": ospic.img.url, },
                        ]}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return render(request, 'sample_os_pic_add.html', {'sample': sample, 'previous_url': previous_url})


@method_decorator([login_required], name='dispatch')
class SampleospicsCollection(ListView):
    model = Sample_os_pics
    context_object_name = 'os_pics'
    template_name = 'sample_os_pics_collection.html'

    def get_queryset(self):
        sample = get_object_or_404(Sample, pk=self.kwargs['pk'])
        queryset = sample.os_pics.all()
        return queryset

    def get_context_data(self, **kwargs):
        sample = get_object_or_404(Sample, pk=self.kwargs['pk'])
        # previous_url = self.request.META.get('HTTP_REFERER')
        # kwargs['previous_url'] = previous_url
        preurl = self.kwargs['preurl']
        kwargs['sample'] = sample
        kwargs['preurl'] = preurl
        return super().get_context_data(**kwargs)


@method_decorator([login_required], name='dispatch')
class SamplesizespecDelete(DeleteView):
    model = Sample_size_specs
    pk_url_kwarg = 'sample_sizespec_pk'
    context_object_name = 'samplesizespec'
    template_name = 'sample_sizespec_delete.html'

    def get_success_url(self):
        sample = self.object.sample
        previous_url = self.request.POST.get('previous_url')
        if "step2" in previous_url:
            return reverse_lazy('sample:sampleaddstep2', kwargs={'pk': sample.pk})
        else:
            return reverse_lazy('sample:sampleedit', kwargs={'pk': sample.pk})

    def get_context_data(self, **kwargs):
        previous_url = self.request.META.get('HTTP_REFERER')
        kwargs['previous_url'] = previous_url
        return super().get_context_data(**kwargs)


@method_decorator([login_required], name='dispatch')
class SampleosavatarDelete(DeleteView):
    model = Sample_os_avatar
    pk_url_kwarg = 'sample_osavatar_pk'
    context_object_name = 'sample_osavatar'
    template_name = 'sample_osavatar_delete.html'

    def get_success_url(self):
        sample = self.object.sample
        previous_url = self.request.POST.get('previous_url')
        if "step2" in previous_url:
            return reverse_lazy('sample:sampleaddstep2', kwargs={'pk': sample.pk})
        else:
            return reverse_lazy('sample:sampleedit', kwargs={'pk': sample.pk})

    def get_context_data(self, **kwargs):
        previous_url = self.request.META.get('HTTP_REFERER')
        kwargs['previous_url'] = previous_url
        return super().get_context_data(**kwargs)


@login_required
def samplesizespecadd(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    previous_url = request.META.get('HTTP_REFERER')
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
        return render(request, 'sample_size_spec_add.html', {'sample': sample, 'previous_url': previous_url})

# sample os avatar upload


@login_required
def sampleosavataradd(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    previous_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = SampleosavatarForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                osavatar = form.save(commit=False)
                osavatar.sample = sample
                osavatar.save()
                data = {"files": [{
                        "name": osavatar.img.name,
                        "url": osavatar.img.url, },
                        ]}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return render(request, 'sample_os_avatar_add.html', {'sample': sample, 'previous_url': previous_url})

# sample swatch add


@login_required
def sampleswatchadd(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    if request.method == 'POST':
        form = SampleswatchForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                swatch = form.save(commit=False)
                swatch.sample = sample
                swatch.save()
                data = {"files": [{
                        "name": swatch.img.name,
                        "url": swatch.img.url, },
                        ]}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return render(request, 'sample_swatch_add.html', {'sample': sample})


@method_decorator([login_required], name='dispatch')
class SampleswatchCollection(ListView):
    model = Sample_swatches
    context_object_name = 'swatches'
    template_name = 'sample_swatch_collection.html'

    def get_queryset(self):
        sample = get_object_or_404(Sample, pk=self.kwargs['pk'])
        queryset = sample.swatches.all()
        return queryset

    def get_context_data(self, **kwargs):
        sample = get_object_or_404(Sample, pk=self.kwargs['pk'])
        kwargs['sample'] = sample
        return super().get_context_data(**kwargs)


@method_decorator([login_required], name='dispatch')
class SampleswatchDelete(DeleteView):
    model = Sample_swatches
    pk_url_kwarg = 'sample_swatch_pk'
    context_object_name = 'swatch'
    template_name = 'sample_swatch_delete.html'

    def get_success_url(self):
        sample = self.object.sample
        return reverse_lazy('sample:sampleswatchcollection', kwargs={'pk': sample.pk})

    def get_context_data(self, **kwargs):
        sample = get_object_or_404(Sample, pk=self.kwargs['pk'])
        kwargs['sample'] = sample
        return super().get_context_data(**kwargs)

# sample factory pics function


@login_required
def samplefpicsadd(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    if request.method == 'POST':
        form = SamplefpicsForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                fpics = form.save(commit=False)
                fpics.sample = sample
                fpics.save()
                data = {"files": [{
                        "name": fpics.img.name,
                        "url": fpics.img.url, },
                        ]}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return render(request, 'sample_fpics_add.html', {'sample': sample})


@method_decorator([login_required], name='dispatch')
class SamplefpicsCollection(ListView):
    model = Sample_pics_factory
    context_object_name = 'fpics'
    template_name = 'sample_fpics_collection.html'

    def get_queryset(self):
        sample = get_object_or_404(Sample, pk=self.kwargs['pk'])
        queryset = sample.factory_pics.all()
        return queryset

    def get_context_data(self, **kwargs):
        sample = get_object_or_404(Sample, pk=self.kwargs['pk'])
        kwargs['sample'] = sample
        return super().get_context_data(**kwargs)


@method_decorator([login_required], name='dispatch')
class SamplefpicDelete(DeleteView):
    model = Sample_pics_factory
    pk_url_kwarg = 'sample_fpic_pk'
    context_object_name = 'fpic'
    template_name = 'sample_fpic_delete.html'

    def get_success_url(self):
        sample = self.object.sample
        return reverse_lazy('sample:samplefpicscollection', kwargs={'pk': sample.pk})

    def get_context_data(self, **kwargs):
        sample = get_object_or_404(Sample, pk=self.kwargs['pk'])
        kwargs['sample'] = sample
        return super().get_context_data(**kwargs)

# sample quotation


@login_required
def samplequotationadd(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    if request.method == 'POST':
        form = SampleoquotationForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                quotation = form.save(commit=False)
                quotation.sample = sample
                quotation.save()
                data = {"files": [{
                        "name": quotation.file.name,
                        "url": quotation.file.url, },
                        ]}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return render(request, 'sample_quotation_add.html', {'sample': sample})


@method_decorator([login_required], name='dispatch')
class SamplequotationDelete(DeleteView):
    model = Sample_quotation_form
    pk_url_kwarg = 'sample_quotation_pk'
    context_object_name = 'sample_quotation'
    template_name = 'sample_quotation_delete.html'

    def get_success_url(self):
        sample = self.object.sample
        return reverse_lazy('sample:sampleedit', kwargs={'pk': sample.pk})

# sample sizespec factory


@login_required
def samplesizespecfadd(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    if request.method == 'POST':
        form = SampleosizespecfForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                sizespecf = form.save(commit=False)
                sizespecf.sample = sample
                sizespecf.save()
                data = {"files": [{
                        "name": sizespecf.file.name,
                        "url": sizespecf.file.url, },
                        ]}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return render(request, 'sample_sizespecf_add.html', {'sample': sample})


@method_decorator([login_required], name='dispatch')
class SamplesizespecfDelete(DeleteView):
    model = Sample_size_spec_factory
    pk_url_kwarg = 'sample_sizespecf_pk'
    context_object_name = 'sample_sizespecf'
    template_name = 'sample_sizespecf_delete.html'

    def get_success_url(self):
        sample = self.object.sample
        return reverse_lazy('sample:sampleedit', kwargs={'pk': sample.pk})


class SampleDetail(TemplateView):
    template_name = 'sample_list.html'


class SampleDelete(DeleteView):
    model = Sample
    context_object_name = 'sample'
    template_name = 'sample_delete.html'
    success_url = reverse_lazy('sample:samplelist')

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
