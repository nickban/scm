from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import (TemplateView,
                                  CreateView, ListView, UpdateView, DetailView,
                                  DeleteView)
from scm.models import (Order, Order_bulk_fabric, Order_fitting_sample,
                        Order_shipping_sample, User, Post, PostAttachment, Sample,
                        Sample_os_pics, Mainlabel,
                     Sample_size_specs, Sample_os_avatar,
                     Sample_swatches, Sample_quotation_form,
                     Sample_pics_factory, Sample_size_spec_factory)
from scm.forms import (SignUpForm, NewpostForm, PostAttachmentForm, FactoryForm,
                    NewsampleForm, SampleForm, SamplesizespecsForm,
                    SampleosavatarForm, SampleospicsForm,
                    SampleswatchForm, SamplefpicsForm,
                    SampledetailForm, MainlabelForm)
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import reverse_lazy
from scm.decorators import (office_required, merchandiser_required, factory_required,
                            o_m_mg_or_required)
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views import View
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages


@login_required
def home(request):
    loginuser = request.user
    posts = Post.objects.all().order_by('-create_time')[0:3]
    posts = list(posts)
    # 有问题的大货布进度记录对应的订单列表['orderid']
    bulk_fabric_p = Order_bulk_fabric.objects.filter(status="WARNING").values_list('order', flat=True)
    print(bulk_fabric_p)
    # 有大货布问题的订单
    orders_bulk_fabric_p = Order.objects.filter(pk__in=bulk_fabric_p)
    print(orders_bulk_fabric_p)
    # 有问题的生产办进度记录对应的订单列表['orderid']
    fitting_p = Order_fitting_sample.objects.filter(status="WARNING").values_list('order', flat=True)
    print(fitting_p)
    # 有生产板问题的订单
    orders_fitting_p = Order.objects.filter(pk__in=fitting_p)
    print(orders_fitting_p)
    # 有问题的船头板进度记录对应的订单列表['orderid']
    shipping_p = Order_shipping_sample.objects.filter(status="WARNING").values_list('order', flat=True)
    print(shipping_p)
    # 有船头板问题的订单
    orders_shipping_p = Order.objects.filter(pk__in=shipping_p)
    print(orders_shipping_p)

    if loginuser.is_factory:
        samples = Sample.objects.filter(Q(factory=loginuser.factory), Q(status="SENT_F"))
        samplesnumber = samples.count()
        ordersnotc = Order.objects.filter(Q(factory=loginuser.factory), Q(status='SENT_FACTORY'))
        ordernumbernotc = ordersnotc.count()
        orders_bulk_fabric_p = orders_bulk_fabric_p.filter(Q(factory=loginuser.factory), Q(status="SENT_FACTORY"))
        orders_bulk_fabric_p_number = orders_bulk_fabric_p.count()
        orders_fitting_p = orders_fitting_p.filter(Q(factory=loginuser.factory), Q(status="SENT_FACTORY"))
        orders_fitting_p_number = orders_fitting_p.count()
        orders_shipping_p = orders_shipping_p.filter(Q(factory=loginuser.factory), Q(status="SENT_FACTORY"))
        orders_shipping_p_number = orders_shipping_p.count()

    elif loginuser.is_merchandiser:
        samples = Sample.objects.filter(Q(merchandiser=loginuser.merchandiser), (Q(status="NEW") | Q(status="SENT_F")))
        samplesnumber = samples.count()
        ordersnotc = Order.objects.filter(Q(merchandiser=loginuser.merchandiser), (Q(status='NEW') | Q(status='SENT_FACTORY')))
        ordernumbernotc = ordersnotc.count()
        orders_bulk_fabric_p = orders_bulk_fabric_p.filter(merchandiser=loginuser.merchandiser)
        orders_bulk_fabric_p_number = orders_bulk_fabric_p.count()
        orders_fitting_p = orders_fitting_p.filter(merchandiser=loginuser.merchandiser)
        orders_fitting_p_number = orders_fitting_p.count()
        orders_shipping_p = orders_shipping_p.filter(merchandiser=loginuser.merchandiser)
        orders_shipping_p_number = orders_shipping_p.count()
    else:
        samples = Sample.objects.filter(Q(status="NEW") | Q(status="SENT_F"))
        samplesnumber = samples.count()
        ordersnotc = Order.objects.filter(Q(status='NEW') | Q(status='SENT_FACTORY'))
        ordernumbernotc = ordersnotc.count()
        orders_bulk_fabric_p_number = orders_bulk_fabric_p.count()
        orders_fitting_p_number = orders_fitting_p.count()
        orders_shipping_p_number = orders_shipping_p.count()

    return render(request, 'home.html', {'samplesnumber': samplesnumber,
                                         'ordernumbernotc': ordernumbernotc,
                                         'posts': posts,
                                         'orders_bulk_fabric_p_number': orders_bulk_fabric_p_number,
                                         'orders_fitting_p_number': orders_fitting_p_number,
                                         'orders_shipping_p_number': orders_shipping_p_number})


@login_required
@factory_required
def setting(request):
    loginuser = request.user
    user = loginuser
    factory = user.factory
    form = FactoryForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            factory = form.save(commit=False)
            factory.user = user
            factory.save()
            return redirect('home')
    else:
        form = FactoryForm(instance=factory)
    return render(request, 'setting.html', {'form': form})


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    # 保存的逻辑写在form的save里
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')


@method_decorator([login_required], name='dispatch')
class Syssetting(TemplateView):
    template_name = 'syssetting.html'


class MainLabel(ListView):
    model = Mainlabel
    ordering = ('brand',)
    context_object_name = 'mainlabels'
    template_name = 'syssetting.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['type'] = 'mainlabel'
        return super().get_context_data(**kwargs)


class MainLabelAdd(CreateView):
    model = Mainlabel
    form_class = MainlabelForm
    template_name = 'mainlabel.html'

    def form_valid(self, form):
        form.save()
        return redirect('mainlabel')


# 修改主唛
@method_decorator([login_required], name='dispatch')
class MainLabelUpdate(UpdateView):
    model = Mainlabel
    form_class = MainlabelForm
    template_name = 'mainlabel.html'

    def form_valid(self, form):
        form.save()
        return redirect('mainlabel')


# 主唛删除
@login_required
def mainlabeldelete(request, pk):
    mainlabel = get_object_or_404(Mainlabel, pk=pk)
    mainlabel.delete()
    return redirect('mainlabel')


class Tag(ListView):
    pass


class AdditionTag(ListView):
    pass


