from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView
from scm.models import (Order, Order_color_ratio_qty, Order_avatar,
                        Order_swatches, Order_size_specs,
                        Order_shipping_pics, Order_packing_ctn, Invoice)
from scm.forms import (
                       OrderForm, Order_color_ratio_qty_Form,
                       OrderavatarForm, OrdersizespecsForm,
                       OrderswatchForm, OrdershippingpicsForm,
                       OrderpackingctnForm, InvoiceSearchForm, InvoiceForm,
                       OrderfittingsampleForm)
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
from django.db.models import F, Sum, IntegerField
from time import strftime
from datetime import datetime, timedelta
from django.template.loader import render_to_string


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
        type = self.kwargs.get('type')
        kwargs['listtype'] = 'new'
        kwargs['type'] = type
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
        kwargs['type'] = type
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

# 上传发票
@login_required
def invoiceattachadd(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, request.FILES, instance=invoice)
        if request.FILES:
            try:
                invoice.file.delete()
            except ObjectDoesNotExist:
                pass
        if form.is_valid():
            invoice = form.save()
            data = {"files": [{
                        "name": invoice.file.name,
                        "url": invoice.file.url, },
                        ]}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        return render(request, 'invoice_attach_add.html', {'invoice': invoice})



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


# 获取实际出货数量
def getacutalcolorqty(pk):
    actualorderqty = []
    colorobject = {}
    order = get_object_or_404(Order, pk=pk)
    colors = order.colorqtys.all()
    for color in colors:
        qty = color.packing_ctns.annotate(eachitemtotalbags=F('bags')*F('totalboxes'))
        qty = qty.aggregate(totalbags=Sum('eachitemtotalbags'), size1=Sum('size1'),
                            size2=Sum('size2'), size3=Sum('size3'), size4=Sum('size4'), size5=Sum('size5'),
                            totalqty=Sum('totalqty'))
        # print(qty)
        colorobject = {'color': color, 'qty': qty}
        # print(colorobject)
        actualorderqty.append(colorobject)
        # print(actualorderqty)
    return actualorderqty


# 创建装箱单
def packinglistadd(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderpackingctnForm(request.POST, order=order)
    colorqtys = order.colorqtys.all()
    packing_ctns = order.packing_ctns.all()
    orderctnsum = order.packing_ctns.annotate(eachitemtotalbags=F('bags')*F('totalboxes'))
    orderctnsum = orderctnsum.aggregate(totalboxes=Sum('totalboxes'), totalbags=Sum('eachitemtotalbags'), size1=Sum('size1'),
                                        size2=Sum('size2'), size3=Sum('size3'), size4=Sum('size4'), size5=Sum('size5'),
                                        totalqty=Sum('totalqty'))
    actualqty = getacutalcolorqty(order.pk)
    # print(actualqty)
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
                                                    'packing_ctns': packing_ctns,
                                                    'orderctnsum': orderctnsum,
                                                    'actualqty': actualqty})


def packinglistsubmit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    packing_status = order.packing_status
    # 获取颜色
    colors = order.colorqtys.all()
    for color in colors:
        # 红色数量
        colorqty = color.qty
        # 红色所有箱对象
        colorboxqs = Order_packing_ctn.objects.filter(color=color)
        if colorboxqs.exists():
            # 每个对象加汇总字段
            colorboxqs = colorboxqs.annotate(totalpcs=F('size1') + F('size2') + F('size3') + F('size4') + F('size5'))
            # 汇总所有对象总件数等于实际颜色的件数
            actualqty = colorboxqs.aggregate(colortotalpcs=Sum('totalpcs', output_field=IntegerField()))
            # 取值
            actualqty = actualqty['colortotalpcs']
            print(actualqty)
            if colorqty in range(401):
                if actualqty in range(int(colorqty*0.9), int(colorqty*1.1) + 1):
                    packing_status.status = 'SUBMIT'
                    packing_status.save()
                else:
                    messages.warning(request, '每个颜色的订单数小于400件，只能接受正负10%!')
                    return redirect('order:packinglistadd', pk=order.pk)
            else:
                if actualqty in range(int(colorqty*0.95), int(colorqty*1.05) + 1):
                    if actualqty <= colorqty + 50:
                        packing_status.status = 'SUBMIT'
                        packing_status.save()
                    else:
                        messages.warning(request, '每个颜色的订单数大于400件，只能接受正负5%，最多接受50件!')
                        return redirect('order:packinglistadd', pk=order.pk)
                else:
                    messages.warning(request, '每个颜色的订单数大于400件，只能接受正负5%，最多接受50件!')
                    return redirect('order:packinglistadd', pk=order.pk)
        else:
            messages.warning(request, "{}没有添加装箱单.".format(color.color_cn))
            return redirect('order:packinglistadd', pk=order.pk)
    return redirect('order:packinglistdetail', pk=order.pk)


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
    actualqty = getacutalcolorqty(order.pk)
    orderctnsum = order.packing_ctns.annotate(eachitemtotalbags=F('bags')*F('totalboxes'))
    orderctnsum = orderctnsum.aggregate(totalboxes=Sum('totalboxes'), totalbags=Sum('eachitemtotalbags'), size1=Sum('size1'),
                                        size2=Sum('size2'), size3=Sum('size3'), size4=Sum('size4'), size5=Sum('size5'),
                                        totalqty=Sum('totalqty'))

    return render(request, 'packinglist_detail.html', {'order': order,
                                                       'colorqtys': colorqtys,
                                                       'packing_ctns': packing_ctns,
                                                       'actualqty': actualqty,
                                                       'orderctnsum': orderctnsum})


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


# 查订单比列
def getratio(request):
    colorratio_pk = request.GET.get('color', None)
    colorratio = get_object_or_404(Order_color_ratio_qty, pk=colorratio_pk)
    ratio = colorratio.ratio
    ratiolist = ratio.split(":")
    ratiolist = list(map(int, ratiolist))
    data = {
        'ratio': ratiolist
    }
    return JsonResponse(data)


def increment_invoice_number():
    last_invoice = Invoice.objects.all().order_by('id').last()
    if not last_invoice:
        return '000001'
    invoice_no = last_invoice.invoice_no
    invoice_no_new = invoice_no[9:]
    print(invoice_no_new)
    new_invoice_no = str(int(invoice_no_new) + 1)
    new_invoice_no = invoice_no_new[0:-(len(new_invoice_no))] + new_invoice_no
    print(new_invoice_no)
    return new_invoice_no


@factory_required
def invoiceadd(request):
    qs = []
    orderlist = {}
    totalpaidamount = 0
    orderpklist = request.POST.getlist('orderpk')
    if not orderpklist:
        return redirect('order:invoicelist')
    else:
        orderlist = Order.objects.in_bulk(orderpklist)
        orderlist = orderlist.values()
        datelist = [order.handover_date_f for order in orderlist]
        mindate = min(datelist)
        maxdate = max(datelist)
        start_of_week = mindate - timedelta(days=mindate.weekday())   # Monday
        end_of_week = start_of_week + timedelta(days=6)   # Sunday
        new_invoiceno = increment_invoice_number()
        if maxdate >= start_of_week and maxdate <= end_of_week:
            invoiceno = mindate.strftime("%Y%m%d") + '_' + new_invoiceno
            factory = request.user.factory
            invoice = Invoice.objects.create(invoice_no=invoiceno, factory=factory,
                                             handoverdate=mindate, start_of_week=start_of_week,
                                             end_of_week=end_of_week)
            for order in orderlist:
                totalqty = order.packing_ctns.aggregate(totalqty=Sum('totalqty', output_field=IntegerField()))
                totalqty = totalqty.get('totalqty')
                paidamount = totalqty * order.factory_price
                totalpaidamount = totalpaidamount + paidamount
                orderobject = {'order': order, 'totalqty': totalqty, 'paidamount': paidamount}
                qs.append(orderobject)
                order.invoice = invoice
                order.save()
        else:
            messages.warning(request, '请把同一周出货的订单创建在一张发票里！')
            return redirect('order:invoicelist')

    return render(request, 'invoice_detail.html', {'qs': qs, 'invoice': invoice, 'factory': factory, 'totalpaidamount': totalpaidamount})


def invoicedelete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    Order.objects.filter(invoice=invoice).update(invoice=None)
    return redirect('order:invoicelist')


def invoicedetail(request, pk):
    qs = []
    totalpaidamount = 0
    invoice = get_object_or_404(Invoice, pk=pk)
    orderqs = Order.objects.filter(invoice=invoice)
    factory = invoice.factory
    for order in orderqs:
        totalqty = order.packing_ctns.aggregate(totalqty=Sum('totalqty', output_field=IntegerField()))
        totalqty = totalqty.get('totalqty')
        paidamount = totalqty * order.factory_price
        totalpaidamount = totalpaidamount + paidamount
        orderobject = {'order': order, 'totalqty': totalqty, 'paidamount': paidamount}
        qs.append(orderobject)
    return render(request, 'invoice_detail.html', {'qs': qs, 'invoice': invoice, 'factory': factory, 'totalpaidamount': totalpaidamount})


def invoicelist(request):
    loginuser = request.user
    if loginuser.is_factory:
        invoiceqs = Invoice.objects.filter(factory=loginuser.factory)
        orderqs = Order.objects.filter(Q(factory=loginuser.factory), Q(status='SHIPPED'), Q(invoice=None))
        return render(request, 'invoice_list.html',  {'invoiceqs': invoiceqs, 'orderqs': orderqs})
    else:
        if request.method == 'POST':
            if request.POST.get('start_handover_date_f') and request.POST.get('end_handover_date_f') and request.POST.get('factory'):
                form = InvoiceSearchForm(request.POST)
                if form.is_valid():
                    factory = form.cleaned_data['factory']
                    start_handover_date_f = form.cleaned_data['start_handover_date_f']
                    end_handover_date_f = form.cleaned_data['end_handover_date_f']
                    invoiceqs = Invoice.objects.filter(factory=factory, handoverdate__range=(start_handover_date_f, end_handover_date_f))
                    print(invoiceqs)
            elif request.POST.get('start_handover_date_f') and request.POST.get('end_handover_date_f'):
                print(1)
                form = InvoiceSearchForm(request.POST)
                print(2)
                print(request.POST.get('start_handover_date_f'))
                print(request.POST.get('end_handover_date_f'))

                if form.is_valid():
                    print(3)
                    start_handover_date_f = form.cleaned_data['start_handover_date_f']
                    end_handover_date_f = form.cleaned_data['end_handover_date_f']
                    invoiceqs = Invoice.objects.filter(handoverdate__range=(start_handover_date_f, end_handover_date_f))
                    print(invoiceqs)
            elif request.POST.get('factory'):
                form = InvoiceSearchForm(request.POST)
                if form.is_valid():
                    factory = form.cleaned_data['factory']
                    invoiceqs = Invoice.objects.filter(factory=factory)
                    print(invoiceqs)

            else:
                messages.warning(request, '请选择开始和结束工厂入仓日期！')
                return redirect('order:invoicelist')
            orderqs = Order.objects.filter(Q(status='SHIPPED'), Q(invoice=None))
        else:
            form = InvoiceSearchForm()
            invoiceqs = Invoice.objects.filter()
            orderqs = Order.objects.filter(Q(status='SHIPPED'), Q(invoice=None))

        return render(request, 'invoice_list.html',  {'invoiceqs': invoiceqs, 'orderqs': orderqs, 'form': form})


def invoicepay(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.status = 'PAID'
    invoice.save()
    return redirect('order:invoicelist')


def orderprogress(request, pk):
    pass


def orderbulkfabric(request, pk):
    pass





def ordershippingsample(request, pk):
    pass


def orderchildorder(request, pk):
    pass


class FunctionList(TemplateView):
    template_name = 'function_list.html'


def orderfittingsample(request, pk):
    pk = pk
    print(pk)
    data = dict()
    order = get_object_or_404(Order, pk=pk)
    print(order)
    if request.method == 'POST':
        print(2)
        form = OrderfittingsampleForm(request.POST)
        if form.is_valid():
            print(3)
            fittingsample = form.save(commit=False)
            print(4)
            fittingsample.order = order
            print(5)
            fittingsample.save()
            print(6)
            data['form_is_valid'] = True
            print(7)
            qs = order.fittingsamples.all()
            print(8)
            data['html_fs_list'] = render_to_string('fs_list.html', {'qs': qs})
        else:
            data['form_is_valid'] = False
    else:
        form = OrderfittingsampleForm()
    context = {'form': form, 'pk': pk}
    print(1)
    data['html_form'] = render_to_string('fs_create_form.html',
                                         context,
                                         request=request)
    data['pk'] = pk
    return JsonResponse(data)
