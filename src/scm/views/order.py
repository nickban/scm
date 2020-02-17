from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView
from scm.models import (Order, Order_color_ratio_qty, Order_avatar,
                        Order_swatches, Order_size_specs,
                        Order_shipping_pics, Order_packing_ctn)
from scm.forms import (
                       OrderForm, Order_color_ratio_qty_Form,
                       OrderavatarForm, OrdersizespecsForm,
                       OrderswatchForm, OrdershippingpicsForm,
                       OrderpackingctnForm)
from django.contrib.auth.decorators import login_required
from scm.decorators import m_mg_or_required, factory_required, office_required, order_is_shipped
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.views import reverse_lazy
from scm.filters import OrderFilter


# 订单列表-未确认(新建，已送工厂状态)
@method_decorator([login_required], name='dispatch')
class OrderListNew(ListView):
    model = Order
    ordering = ('-created_date', )
    context_object_name = 'orders'
    template_name = 'order_list.html'

    def get_queryset(self):
        loginuser = self.request.user
        if loginuser.is_merchandiser:
            return Order.objects.filter(Q(merchandiser=loginuser.merchandiser),
                                        Q(status='NEW') | Q(status='SENT_FACTORY')).order_by('-created_date')
        elif loginuser.is_factory:
            return Order.objects.filter(Q(factory=loginuser.factory), Q(status='SENT_FACTORY')).order_by('-created_date')
        else:
            return Order.objects.filter(Q(status='NEW') | Q(status='SENT_FACTORY')).order_by('-created_date')

    def get_context_data(self, **kwargs):
        kwargs['listtype'] = 'new'
        return super().get_context_data(**kwargs)

# 订单列表-已确认(已确认状态)
@method_decorator([login_required], name='dispatch')
class OrderListConfrimed(ListView):
    model = Order
    ordering = ('-created_date', )
    context_object_name = 'orders'
    template_name = 'order_list.html'

    def get_queryset(self):
        loginuser = self.request.user
        if loginuser.is_merchandiser:
            return Order.objects.filter(Q(merchandiser=loginuser.merchandiser),
                                        Q(status='CONFIRMED'))
        elif loginuser.is_factory:
            return Order.objects.filter(Q(factory=loginuser.factory),
                                        Q(status='CONFIRMED'))
        else:
            return Order.objects.filter(status='CONFIRMED')

    def get_context_data(self, **kwargs):
        kwargs['listtype'] = 'confirmed'
        return super().get_context_data(**kwargs)


# 订单列表-已出货(已出货状态)
@method_decorator([login_required], name='dispatch')
class OrderListShipped(ListView):
    model = Order
    ordering = ('-created_date', )
    context_object_name = 'orders'
    template_name = 'order_list.html'

    def get_queryset(self):
        loginuser = self.request.user
        if loginuser.is_merchandiser:
            return Order.objects.filter(Q(merchandiser=loginuser.merchandiser),
                                        Q(status='SHIPPED'))
        elif loginuser.is_factory:
            return Order.objects.filter(Q(factory=loginuser.factory),
                                        Q(status='SHIPPED'))
        else:
            return Order.objects.filter(status='SHIPPED')

    def get_context_data(self, **kwargs):
        kwargs['listtype'] = 'shipped'
        return super().get_context_data(**kwargs)

# 订单新建
@method_decorator([login_required, m_mg_or_required], name='dispatch')
class OrderAdd(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_edit.html'

    def form_valid(self, form):
        order = form.save()
        messages.success(self.request, '订单创建成功!')
        return redirect('order:orderedit', pk=order.pk)

# 订单编辑
@method_decorator([login_required, order_is_shipped, m_mg_or_required], name='dispatch')
class OrderEdit(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_edit.html'
    context_object_name = 'order'

    def form_valid(self, form):
        order = form.save()
        return redirect('order:orderedit', pk=order.pk)

    def get_context_data(self, **kwargs):
        kwargs['swatches'] = self.get_object().swatches.all()
        kwargs['shippingpics'] = self.get_object().shippingpics.all()
        kwargs['sizespecs'] = self.get_object().sizespecs.all()
        try:
            kwargs['colorqtys'] = self.get_object().colorqtys.all().order_by('-created_date')
        except ObjectDoesNotExist:
            kwargs['colorqtys'] = ''
        return super().get_context_data(**kwargs)


# 订单详情，工厂查看页面
@login_required
def orderdetail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    swatches = order.swatches.all()
    sizespecs = order.sizespecs.all()
    shippingpics = order.shippingpics.all()
    colorqtys = order.colorqtys.all()
    return render(request, 'order_detail.html', {'order': order, 'swatches': swatches,
                                                 'sizespecs': sizespecs, 'shippingpics': shippingpics,
                                                 'colorqtys': colorqtys})


# 订单颜色数量新增
@login_required
@m_mg_or_required
def colorqtyadd(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = Order_color_ratio_qty_Form(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            colorqty = form.save(commit=False)
            colorqty.order = order
            colorqty.save()
            return redirect('order:orderedit', pk=order.pk)
    else:
        form = Order_color_ratio_qty_Form()
    return render(request, 'colorqty_add.html', {'form': form, 'order': order})


# 订单颜色数量更改
@login_required
@m_mg_or_required
def colorqtyedit(request, pk, colorqtypk):
    order = get_object_or_404(Order, pk=pk)
    colorqty = get_object_or_404(Order_color_ratio_qty, pk=colorqtypk)
    form = Order_color_ratio_qty_Form(request.POST, instance=colorqty)
    if request.method == 'POST':
        if form.is_valid():
            colorqty = form.save(commit=False)
            colorqty.order = order
            colorqty.save()
            return redirect('order:orderedit', pk=order.pk)
    else:
        form = Order_color_ratio_qty_Form(instance=colorqty)
    return render(request, 'colorqty_add.html', {'form': form, 'order': order})


# 订单颜色数量删除
@login_required
@m_mg_or_required
def colorqtydelete(request, pk, colorqtypk):
    order = get_object_or_404(Order, pk=pk)
    colorqty = get_object_or_404(Order_color_ratio_qty, pk=colorqtypk)
    colorqty.delete()
    return redirect('order:orderedit', pk=order.pk)


# 删除订单
@method_decorator([login_required, m_mg_or_required], name='dispatch')
class OrderDelete(DeleteView):
    model = Order
    context_object_name = 'order'
    template_name = 'order_delete.html'

    def get_success_url(self):
        order = self.get_object()
        if order.status == 'NEW' or order.status == 'SENT_FACTORY':
            success_url = reverse_lazy('order:orderlistnew')
            return success_url
        elif order.status == 'CONFIRMED':
            success_url = reverse_lazy('order:orderlistconfirmed')
            return success_url
        else:
            success_url = reverse_lazy('order:orderlistshipped')
            return success_url


# 拷贝订单，测试数据用
@login_required
@m_mg_or_required
def ordercopy(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.pk = None
    order.save()
    return redirect('order:orderedit', pk=order.pk)


# 改变订单状态到送工厂状态
@login_required
@m_mg_or_required
def ordersentfactory(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.factory is None:
        messages.warning(request, '请选择工厂并保存后，才能通知工厂!')
    else:
        order.status = "SENT_FACTORY"
        order.save()
        messages.success(request, '订单已经安排给工厂，并已邮件通知!')
    return redirect('order:orderedit', pk=order.pk)


# 订单确认
@login_required
@factory_required
def orderconfirm(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = "CONFIRMED"
    order.save()
    messages.success(request, '已确认订单, 请在确认订单列表查找!')
    return redirect('order:orderdetail', pk=order.pk)


# 订单出货
@login_required
@office_required
def ordershipped(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = "SHIPPED"
    order.save()
    messages.success(request, '订单已出货, 请在出货订单列表查找!')
    return redirect('order:orderedit', pk=order.pk)


# 订单附件通用功能视图
@login_required
def orderattachadd(request, pk, attachtype):
    order = get_object_or_404(Order, pk=pk)
    if attachtype == 'avatar':
        if request.FILES:
            try:
                order.avatar.delete()
            except ObjectDoesNotExist:
                pass
            form = OrderavatarForm(request.POST, request.FILES)
    elif attachtype == 'sizespecs':
        form = OrdersizespecsForm(request.POST, request.FILES)
    elif attachtype == 'swatch':
        form = OrderswatchForm(request.POST, request.FILES)
    else:
        form = OrdershippingpicsForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            with transaction.atomic():
                attach = form.save(commit=False)
                attach.order = order
                attach.save()
                data = {"files": [{
                            "name": attach.file.name,
                            "url": attach.file.url, },
                            ]}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return render(request, 'order_attach_add.html', {'order': order, 'attachtype': attachtype})


@login_required
def orderattachdelete(request, pk, attachtype, attach_pk):
    order = get_object_or_404(Order, pk=pk)
    attachtype = attachtype
    if attachtype == 'avatar':
        attach = get_object_or_404(Order_avatar, pk=attach_pk)
        attach.delete()
        return redirect('order:orderedit', pk=order.pk)
    elif attachtype == 'swatch':
        attach = get_object_or_404(Order_swatches, pk=attach_pk)
        attach.delete()
        return redirect('order:orderattachcollection', pk=order.pk, attachtype=attachtype)
    elif attachtype == 'sizespecs':
        attach = get_object_or_404(Order_size_specs, pk=attach_pk)
        attach.delete()
        return redirect('order:orderedit', pk=order.pk)
    elif attachtype == 'swatch':
        attach = get_object_or_404(Order_swatches, pk=attach_pk)
        attach.delete()
        return redirect('order:orderattachcollection', pk=order.pk, attachtype=attachtype)
    else:
        attach = get_object_or_404(Order_shipping_pics, pk=attach_pk)
        attach.delete()
        return redirect('order:orderattachcollection', pk=order.pk, attachtype=attachtype)


@login_required
def orderattachcollection(request, pk, attachtype):
    order = get_object_or_404(Order, pk=pk)
    attachtype = attachtype
    if attachtype == 'swatch':
        attaches = order.swatches.all()
    else:
        attaches = order.shippingpics.all()
    return render(request, 'order_attach_collection.html', {'order': order,
                  'attachtype': attachtype, 'attaches': attaches})


# 装箱单查找
def plsearch(request):
    loginuser = request.user
    if loginuser.is_factory:
        factory = loginuser.factory
        order_list = Order.objects.filter(Q(factory=factory), Q(status='CONFIRMED') | Q(status='SHIPPED'))
    else:
        order_list = Order.objects.filter(Q(status='CONFIRMED') | Q(status='SHIPPED'))
    order_filter = OrderFilter(request.GET, queryset=order_list)
    return render(request, 'plsearch_list.html', {'filter': order_filter})


# 创建装箱单
def packinglistadd(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderpackingctnForm(request.POST, order=order)
    colorqtys = order.colorqtys.all()
    packing_ctns = order.packing_ctns.all()
    if request.method == 'POST':
        if form.is_valid():
            packinglist = form.save(commit=False)
            packinglist.order = order
            packinglist.save()
        return redirect('order:packinglistadd', pk=order.pk)
    else:
        form = OrderpackingctnForm(order=order)
    return render(request, 'packinglist_add.html', {'form': form,
                                                    'colorqtys': colorqtys,
                                                    'order': order,
                                                    'packing_ctns': packing_ctns})


# 删除装箱单
def packinglistdelete(request, pk, plpk):
    order = get_object_or_404(Order, pk=pk)
    plctn = get_object_or_404(Order_packing_ctn, pk=plpk)
    plctn.delete()
    return redirect('order:packinglistadd', pk=order.pk)


# 装箱单详情
def packinglistdetail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    colorqtys = order.colorqtys.all()
    packing_ctns = order.packing_ctns.all()
    return render(request, 'packinglist_detail.html', {'order': order,
                                                       'colorqtys': colorqtys,
                                                       'packing_ctns': packing_ctns})


def packinglistsubmit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    packing_status = order.packing_status
    packing_status.status = 'SUBMIT'
    packing_status.save()
    return redirect('order:packinglistdetail', pk=order.pk)


def packinglistclose(request, pk):
    order = get_object_or_404(Order, pk=pk)
    packing_status = order.packing_status
    packing_status.status = 'CLOSED'
    packing_status.save()
    return redirect('order:packinglistdetail', pk=order.pk)


def packinglistreset(request, pk):
    order = get_object_or_404(Order, pk=pk)
    packing_status = order.packing_status
    packing_status.status = 'NEW'
    packing_status.save()
    return redirect('order:packinglistadd', pk=order.pk)



class FunctionList(TemplateView):
    template_name = 'function_list.html'


class InvoiceList(TemplateView):
    template_name = 'invoice_list.html'
