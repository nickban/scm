from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView
from scm.models import (User, Order, Order_color_ratio_qty, Order_avatar,
                        Order_swatches, Order_size_specs,
                        Order_shipping_pics, Order_packing_ctn, Invoice,
                        Order_fitting_sample, Order_bulk_fabric, Order_shipping_sample,
                        Order_packing_status, Order_Barcode)
from scm.forms import (
                       OrderForm, Order_color_ratio_qty_Form,
                       OrderavatarForm, OrdersizespecsForm,
                       OrderswatchForm, OrdershippingpicsForm,
                       OrderpackingctnForm, InvoiceSearchForm, InvoiceForm,
                       OrderfittingsampleForm, OrderbulkfabricForm,
                       OrdershippingsampleForm, OrderpackingstatusForm,
                       OrderbarcodeForm)
from django.contrib.auth.decorators import login_required
from scm.decorators import (m_mg_or_required, factory_required, office_required,
                            order_is_shipped, packinglist_is_sented, o_m_mg_or_required)
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.views import reverse_lazy
from django.db.models import F, Sum, IntegerField
from datetime import timedelta
from django.template.loader import render_to_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import smtplib
from decouple import config


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
        # 待确认，应该type没有用到
        # kwargs['type'] = type
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
            pass
        try:
            kwargs['barcode'] = self.get_object().barcode
        except ObjectDoesNotExist:
            pass
        return super().get_context_data(**kwargs)


# 订单详情，工厂查看页面
@login_required
def orderdetail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    swatches = order.swatches.all()
    sizespecs = order.sizespecs.all()
    shippingpics = order.shippingpics.all()
    colorqtys = order.colorqtys.all().order_by('-created_date')
    try:
        barcode = order.barcode
    except ObjectDoesNotExist:
        barcode = None
    return render(request, 'order_detail.html', {'order': order, 'swatches': swatches,
                                                 'sizespecs': sizespecs, 'shippingpics': shippingpics,
                                                 'colorqtys': colorqtys, 'barcode': barcode})


# 订单颜色数量新增
@login_required
@m_mg_or_required
def colorqtyadd(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = Order_color_ratio_qty_Form(request.POST)
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
    if request.method == 'POST':
        form = Order_color_ratio_qty_Form(request.POST, instance=colorqty)
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
        messages.success(request, '订单已经安排给工厂!')
        factoryemail = str(order.factory.email)
        try:
            avatar_file = order.avatar.file
            encoded = base64.b64encode(open(avatar_file.path, "rb").read()).decode()
        except ObjectDoesNotExist:
            encoded = ''
        sender_email = 'SCM@monayoung.com.au'
        receiver_email = factoryemail
        message = MIMEMultipart("alternative")
        message["Subject"] = "缘色SCM-新订单通知"
        message["From"] = sender_email
        message["To"] = receiver_email
        orderpo = order.po
        orderstyleno = order.style_no
        brand = order.brand.name
        merchandiser = order.merchandiser.user.username
        html = f"""\
            <html>
            <body>
            <h3>新订单已经安排给工厂,详细信息请看SCM！</h3>
            <h3>订单号:{orderpo}</h3>
            <h3>款号:{orderstyleno}</h3>
            <h3>品牌:{brand}</h3>
            <h3>跟单:{merchandiser}</h3>
            <h3>图片:</h3>
            <img src="data:image/jpg;base64,{encoded}" width=200px height=200px>
            </body>
            </html>
            """
        part = MIMEText(html, "html")
        message.attach(part)
        with smtplib.SMTP(config('EMAIL_HOST'), config('EMAIL_PORT', cast=int)) as server:
            server.login(config('EMAIL_HOST_USER'), config('EMAIL_HOST_PASSWORD'))
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
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
    totalqty = order.packing_ctns.aggregate(totalqty=Sum('totalqty', output_field=IntegerField()))
    totalqty = totalqty.get('totalqty') or 0
    order.actual_ship_qty = totalqty
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
    elif attachtype == 'barcode':
        if request.FILES:
            try:
                order.barcode.delete()
            except ObjectDoesNotExist:
                pass
            form = OrderbarcodeForm(request.POST, request.FILES)
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
@factory_required
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

# 订单附件删除
@login_required
def orderattachdelete(request, pk, attachtype, attach_pk):
    order = get_object_or_404(Order, pk=pk)
    attachtype = attachtype
    if attachtype == 'avatar':
        attach = get_object_or_404(Order_avatar, pk=attach_pk)
        attach.delete()
        return redirect('order:orderedit', pk=order.pk)
    elif attachtype == 'barcode':
        attach = get_object_or_404(Order_Barcode, pk=attach_pk)
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

# 订单附件集
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


# 装箱单查找，暂时不用，供今后参考
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
    if order.packing_type.shortname == '单件包装':
        for color in colors:
            # 单件包装不用中包,但是可以放到模板里做判断，这样不用写2套模板
            qty = color.packing_ctns.annotate(sumtotalqty=F('totalboxes')*F('totalqty'),
                                              sumsize1=F('totalboxes')*F('size1'),
                                              sumsize2=F('totalboxes')*F('size2'),
                                              sumsize3=F('totalboxes')*F('size3'),
                                              sumsize4=F('totalboxes')*F('size4'),
                                              sumsize5=F('totalboxes')*F('size5'),
                                              )
            qty = qty.aggregate(totalbags=Sum('bags'), size1=Sum('sumsize1'),
                                               size2=Sum('sumsize2'), size3=Sum('sumsize3'),
                                               size4=Sum('sumsize4'), size5=Sum('sumsize5'),
                                               totalqty=Sum('sumtotalqty'))
            colorobject = {'color': color, 'qty': qty}
            actualorderqty.append(colorobject)
    else:
        for color in colors:
            qty = color.packing_ctns.annotate(sumtotalqty=F('totalboxes')*F('totalqty'),
                                              eachitemtotalbags=F('bags')*F('totalboxes'),
                                              sumsize1=F('totalboxes')*F('size1'),
                                              sumsize2=F('totalboxes')*F('size2'),
                                              sumsize3=F('totalboxes')*F('size3'),
                                              sumsize4=F('totalboxes')*F('size4'),
                                              sumsize5=F('totalboxes')*F('size5'),
                                              )
            qty = qty.aggregate(totalbags=Sum('eachitemtotalbags'), size1=Sum('sumsize1'),
                                size2=Sum('sumsize2'), size3=Sum('sumsize3'), size4=Sum('sumsize4'), size5=Sum('sumsize5'),
                                totalqty=Sum('sumtotalqty'))
            colorobject = {'color': color, 'qty': qty}
            actualorderqty.append(colorobject)
    return actualorderqty


# 创建装箱单----创建前检查状态，如果已经提交回到详情页
@login_required
@packinglist_is_sented
def packinglistadd(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderpackingctnForm(request.POST, order=order)
    colorqtys = order.colorqtys.all()
    gross_weight = order.packing_status.gross_weight
    packing_ctns = order.packing_ctns.all()
    packing_ctns = packing_ctns.annotate(gross_weight=F('totalboxes')*gross_weight, sumtotalqty=F('totalboxes')*F('totalqty'))
    orderctnsum = order.packing_ctns.annotate(eachitemtotalbags=F('bags')*F('totalboxes'),
                                              sumtotalqty=F('totalboxes')*F('totalqty'),
                                              gross_weight=F('totalboxes')*gross_weight)
    orderctnsum = orderctnsum.aggregate(totalbags=Sum('eachitemtotalbags'), size1=Sum('size1'),
                                        size2=Sum('size2'), size3=Sum('size3'), size4=Sum('size4'), size5=Sum('size5'),
                                        totalqty=Sum('sumtotalqty'))
    packing_ctns_exclude_share = order.packing_ctns.filter(sharebox=False)
    packing_ctns_exclude_share_grossweight = packing_ctns_exclude_share.annotate(gross_weight=F('totalboxes')*gross_weight)
    totalgrossweight = packing_ctns_exclude_share_grossweight.aggregate(totalgrossweight=Sum('gross_weight'))
    totalgrossweight = totalgrossweight['totalgrossweight']
    totalboxes = packing_ctns_exclude_share.aggregate(totalboxes=Sum('totalboxes'))
    totalboxes = totalboxes['totalboxes']
    actualqty = getacutalcolorqty(order.pk)
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
                                                    'actualqty': actualqty,
                                                    'totalboxes': totalboxes,
                                                    'totalgrossweight': totalgrossweight})


# 提交装箱单
@login_required
@factory_required
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
            colorboxqs = colorboxqs.annotate(sumtotalqty=F('totalboxes')*F('totalqty'))
            # 汇总所有对象总件数等于实际颜色的件数
            actualqty = colorboxqs.aggregate(colortotalpcs=Sum('sumtotalqty', output_field=IntegerField()))
            # 取值
            actualqty = actualqty['colortotalpcs']
            if colorqty in range(401):
                accepted = actualqty in range(int(colorqty*0.9), int(colorqty*1.1) + 1)
                if not accepted:
                    messages.warning(request, '每个颜色的订单数小于400件，只能接受正负10%!')
                    return redirect('order:packinglistadd', pk=order.pk)
            else:
                accepted = actualqty in range(int(colorqty*0.95), int(colorqty*1.05) + 1)
                if not accepted:
                    messages.warning(request, '每个颜色的订单数大于400件，只能接受正负5%，最多接受50件!')
                    return redirect('order:packinglistadd', pk=order.pk)
                else:
                    if (actualqty > colorqty + 50):
                        messages.warning(request, '每个颜色的订单数大于400件，只能接受正负5%，最多接受50件!')
                        return redirect('order:packinglistadd', pk=order.pk)
        else:
            messages.warning(request, "{}没有添加装箱单.".format(color.color_cn))
            return redirect('order:packinglistadd', pk=order.pk)
    packing_status.status = 'SUBMIT'
    packing_status.save()
    # 发邮件，发跟单和行政
    office_emails = User.objects.filter(is_office=True).values_list('email', flat=True)
    office_emails = list(office_emails)
    print(office_emails)
    try:
        avatar_file = order.avatar.file
        encoded = base64.b64encode(open(avatar_file.path, "rb").read()).decode()
    except ObjectDoesNotExist:
        encoded = ''
    sender_email = 'SCM@monayoung.com.au'
    message = MIMEMultipart("alternative")
    message["Subject"] = "缘色SCM-装箱单提交！"
    message["From"] = sender_email
    orderpo =  order.po
    orderstyleno =  order.style_no
    brand = order.brand.name
    factory = order.factory.user.username
    html = f"""\
        <html>
        <body>
        <h3>订单装箱单已提交！</h3>
        <h3>订单号:{orderpo}</h3>
        <h3>款号:{orderstyleno}</h3>
        <h3>品牌:{brand}</h3>
        <h3>工厂:{factory}</h3>
        <h3>图片:</h3>
        <img src="data:image/jpg;base64,{encoded}" width=200px height=200px>
        </body>
        </html>
        """
    part = MIMEText(html, "html")
    message.attach(part)
    with smtplib.SMTP(config('EMAIL_HOST'), config('EMAIL_PORT', cast=int)) as server:
        server.login(config('EMAIL_HOST_USER'), config('EMAIL_HOST_PASSWORD'))
        for email in office_emails:
            message["To"] = email
            server.sendmail(
                sender_email, email, message.as_string()
            )

    return redirect('order:packinglistdetail', pk=order.pk)


# 删除装箱单
@login_required
@factory_required
def packinglistdelete(request, pk, plpk):
    order = get_object_or_404(Order, pk=pk)
    plctn = get_object_or_404(Order_packing_ctn, pk=plpk)
    plctn.delete()
    return redirect('order:packinglistadd', pk=order.pk)


# 装箱单详情
@login_required
def packinglistdetail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    # form = OrderpackingctnForm(request.POST, order=order)
    colorqtys = order.colorqtys.all()
    gross_weight = order.packing_status.gross_weight
    packing_ctns = order.packing_ctns.all()
    packing_ctns = packing_ctns.annotate(gross_weight=F('totalboxes')*gross_weight)
    orderctnsum = order.packing_ctns.annotate(eachitemtotalbags=F('bags')*F('totalboxes'))
    orderctnsum = orderctnsum.aggregate(totalbags=Sum('eachitemtotalbags'), size1=Sum('size1'),
                                        size2=Sum('size2'), size3=Sum('size3'), size4=Sum('size4'), size5=Sum('size5'),
                                        totalqty=Sum('totalqty'))
    packing_ctns_exclude_share = order.packing_ctns.filter(sharebox=False)
    totalboxes = packing_ctns_exclude_share.aggregate(totalboxes=Sum('totalboxes'))
    totalboxes = totalboxes['totalboxes']
    actualqty = getacutalcolorqty(order.pk)

    return render(request, 'packinglist_detail.html', {'order': order,
                                                       'colorqtys': colorqtys,
                                                       'packing_ctns': packing_ctns,
                                                       'actualqty': actualqty,
                                                       'orderctnsum': orderctnsum,
                                                       'totalboxes': totalboxes})

# 确认装箱单
@login_required
@o_m_mg_or_required
def packinglistclose(request, pk):
    order = get_object_or_404(Order, pk=pk)
    packing_status = order.packing_status
    packing_status.status = 'CLOSED'
    packing_status.save()
    return redirect('order:packinglistdetail', pk=order.pk)


# 重置装箱单
@login_required
@o_m_mg_or_required

def packinglistreset(request, pk):
    order = get_object_or_404(Order, pk=pk)
    packing_status = order.packing_status
    packing_status.status = 'NEW'
    packing_status.save()
    return redirect('order:packinglistadd', pk=order.pk)


# 修改纸箱规格
@method_decorator([login_required, factory_required], name='dispatch')
class Update_packingstatus(UpdateView):
    model = Order_packing_status
    form_class = OrderpackingstatusForm
    template_name = 'order_update_packingstatus.html'
    context_object_name = 'packingstatus'

    def form_valid(self, form):
        packingstatus = form.save()
        return redirect('order:packinglistadd', pk=packingstatus.pk)

    def get_context_data(self, **kwargs):
        kwargs['order'] = self.get_object().order
        return super().get_context_data(**kwargs)


# 查订单比列
def getratio(request):
    colorratio_pk = request.GET.get('color', None)
    colorratio = get_object_or_404(Order_color_ratio_qty, pk=colorratio_pk)
    order = colorratio.order
    if order.packing_type.shortname == '单件包装':
        packing_type = 1
        ratiolist = []
    else:
        packing_type = 2
        ratio = colorratio.ratio
        ratiolist = ratio.split(":")
        ratiolist = list(map(int, ratiolist))
    data = {
        'ratio': ratiolist
    }
    data['packing_type'] = packing_type
    return JsonResponse(data)


# 发票号递增规则
def increment_invoice_number():
    last_invoice = Invoice.objects.all().order_by('id').last()
    if not last_invoice:
        return '000001'
    invoice_no = last_invoice.invoice_no
    invoice_no_new = invoice_no[9:]
    new_invoice_no = str(int(invoice_no_new) + 1)
    new_invoice_no = invoice_no_new[0:-(len(new_invoice_no))] + new_invoice_no
    return new_invoice_no

# 创建发票
@login_required
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
        start_of_week = mindate - timedelta(days=mindate.weekday())   # 周一
        end_of_week = start_of_week + timedelta(days=6)   # 周日
        new_invoiceno = increment_invoice_number()
        if maxdate >= start_of_week and maxdate <= end_of_week:
            invoiceno = mindate.strftime("%Y%m%d") + '_' + new_invoiceno
            factory = request.user.factory
            invoice = Invoice.objects.create(invoice_no=invoiceno, factory=factory,
                                             handoverdate=mindate, start_of_week=start_of_week,
                                             end_of_week=end_of_week)
            for order in orderlist:
                totalqty = order.packing_ctns.aggregate(totalqty=Sum('totalqty', output_field=IntegerField()))
                totalqty = totalqty.get('totalqty') or 0
                factory_price = order.factory_price or 0
                paidamount = totalqty * factory_price
                totalpaidamount = totalpaidamount + paidamount
                orderobject = {'order': order, 'totalqty': totalqty, 'paidamount': paidamount}
                qs.append(orderobject)
                order.invoice = invoice
                order.save()
        else:
            messages.warning(request, '请把同一周出货的订单创建在一张发票里！')
            return redirect('order:invoicelist')

    return render(request, 'invoice_detail.html', {'qs': qs, 'invoice': invoice, 'factory': factory, 'totalpaidamount': totalpaidamount})


# 删除发票
@login_required
@factory_required
def invoicedelete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    Order.objects.filter(invoice=invoice).update(invoice=None)
    return redirect('order:invoicelist')


# 发票详情页
def invoicedetail(request, pk):
    qs = []
    totalpaidamount = 0
    invoice = get_object_or_404(Invoice, pk=pk)
    orderqs = Order.objects.filter(invoice=invoice)
    factory = invoice.factory
    for order in orderqs:
        totalqty = order.packing_ctns.aggregate(totalqty=Sum('totalqty', output_field=IntegerField()))
        totalqty = totalqty.get('totalqty') or 0
        factory_price = order.factory_price or 0
        paidamount = totalqty * factory_price
        totalpaidamount = totalpaidamount + paidamount
        orderobject = {'order': order, 'totalqty': totalqty, 'paidamount': paidamount}
        qs.append(orderobject)
    return render(request, 'invoice_detail.html', {'qs': qs, 'invoice': invoice, 'factory': factory, 'totalpaidamount': totalpaidamount})


# 发票列表
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
            elif request.POST.get('start_handover_date_f') and request.POST.get('end_handover_date_f'):
                form = InvoiceSearchForm(request.POST)
                if form.is_valid():
                    start_handover_date_f = form.cleaned_data['start_handover_date_f']
                    end_handover_date_f = form.cleaned_data['end_handover_date_f']
                    invoiceqs = Invoice.objects.filter(handoverdate__range=(start_handover_date_f, end_handover_date_f))
            elif request.POST.get('factory'):
                form = InvoiceSearchForm(request.POST)
                if form.is_valid():
                    factory = form.cleaned_data['factory']
                    invoiceqs = Invoice.objects.filter(factory=factory)
            else:
                messages.warning(request, '请选择开始和结束工厂入仓日期！')
                return redirect('order:invoicelist')
            orderqs = Order.objects.filter(Q(status='SHIPPED'), Q(invoice=None))
        else:
            form = InvoiceSearchForm()
            invoiceqs = Invoice.objects.filter()
            orderqs = Order.objects.filter(Q(status='SHIPPED'), Q(invoice=None))
        return render(request, 'invoice_list.html',  {'invoiceqs': invoiceqs, 'orderqs': orderqs, 'form': form})


# 发票已付款
def invoicepay(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.status = 'PAID'
    invoice.save()
    return redirect('order:invoicelist')


# 发票重置
def invoicereset(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.status = 'NEW'
    invoice.save()
    return redirect('order:invoicelist')

# 生产板进度增加
def fittingsample(request, pk):
    pk = pk
    data = dict()
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderfittingsampleForm(request.POST)
        if form.is_valid():
            fittingsample = form.save(commit=False)
            fittingsample.order = order
            fittingsample.save()
            data['form_is_valid'] = True
            qs = order.fittingsamples.all().order_by('-created_date')
            data['html_fs_list'] = render_to_string('fs_list.html', {'qs': qs})
        else:
            data['form_is_valid'] = False
    else:
        form = OrderfittingsampleForm()
    context = {'form': form, 'pk': pk}
    data['html_form'] = render_to_string('fs_create_form.html',
                                         context,
                                         request=request)
    data['pk'] = pk
    return JsonResponse(data)


# 生产板进度删除
def fsdelete(request, pk):
    data = dict()
    fs = get_object_or_404(Order_fitting_sample, pk=pk)
    order = fs.order
    pk = order.pk
    fs.delete()
    qs = order.fittingsamples.all().order_by('-created_date')
    data['form_is_valid'] = True
    data['html_fs_list'] = render_to_string('fs_list.html', {'qs': qs})
    data['pk'] = pk
    return JsonResponse(data)


# 显示全部生产办进度
def fsall(request, pk):
    data = dict()
    order = get_object_or_404(Order, pk=pk)
    qs = order.fittingsamples.all().order_by('-created_date')
    data['form_is_valid'] = True
    data['html_fs_list'] = render_to_string('fs_list_all.html', {'qs': qs})
    data['pk'] = pk
    return JsonResponse(data)


# 只显示最近3个生产办进度
def fsthree(request, pk):
    data = dict()
    order = get_object_or_404(Order, pk=pk)
    qs = order.fittingsamples.all().order_by('-created_date')
    data['form_is_valid'] = True
    data['html_fs_list'] = render_to_string('fs_list.html', {'qs': qs})
    data['pk'] = pk
    return JsonResponse(data)



# 生产板进度修改
def fsedit(request, pk):
    data = dict()
    fs = get_object_or_404(Order_fitting_sample, pk=pk)
    order = fs.order
    pk = order.pk
    if request.method == 'POST':
        form = OrderfittingsampleForm(request.POST, instance=fs)
        if form.is_valid():
            form.save()
            qs = order.fittingsamples.all().order_by('-created_date')
            data['form_is_valid'] = True
            data['html_fs_list'] = render_to_string('fs_list.html', {'qs': qs})
        else:
            data['form_is_valid'] = False
    else:
        form = OrderfittingsampleForm(instance=fs)
    context = {'form': form, 'pk': fs.pk}
    data['html_form'] = render_to_string('fs_edit_form.html',
                                         context,
                                         request=request)
    data['pk'] = pk
    return JsonResponse(data)


# 大货布进度增加
def bulkfabric(request, pk):
    pk = pk
    data = dict()
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderbulkfabricForm(request.POST)
        if form.is_valid():
            bulkfabric = form.save(commit=False)
            bulkfabric.order = order
            bulkfabric.save()
            data['form_is_valid'] = True
            qs = order.bulkfabrics.all().order_by('-created_date')
            data['html_bf_list'] = render_to_string('bf_list.html', {'qs': qs})
        else:
            data['form_is_valid'] = False
    else:
        form = OrderbulkfabricForm()
    context = {'form': form, 'pk': pk}
    data['html_form'] = render_to_string('bf_create_form.html',
                                         context,
                                         request=request)
    data['pk'] = pk
    return JsonResponse(data)


# 大货布进度删除
def bfdelete(request, pk):
    data = dict()
    bf = get_object_or_404(Order_bulk_fabric, pk=pk)
    order = bf.order
    pk = order.pk
    bf.delete()
    qs = order.bulkfabrics.all().order_by('-created_date')
    data['form_is_valid'] = True
    data['html_bf_list'] = render_to_string('bf_list.html', {'qs': qs})
    data['pk'] = pk
    return JsonResponse(data)


# 大货布进度修改
def bfedit(request, pk):
    data = dict()
    bf = get_object_or_404(Order_bulk_fabric, pk=pk)
    order = bf.order
    pk = order.pk
    if request.method == 'POST':
        form = OrderbulkfabricForm(request.POST, instance=bf)
        if form.is_valid():
            form.save()
            qs = order.bulkfabrics.all().order_by('-created_date')
            data['form_is_valid'] = True
            data['html_bf_list'] = render_to_string('bf_list.html', {'qs': qs})
        else:
            data['form_is_valid'] = False
    else:
        form = OrderbulkfabricForm(instance=bf)
    context = {'form': form, 'pk': bf.pk}
    data['html_form'] = render_to_string('bf_edit_form.html',
                                         context,
                                         request=request)
    data['pk'] = pk
    return JsonResponse(data)


# 船头板进度增加
def shippingsample(request, pk):
    pk = pk
    data = dict()
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrdershippingsampleForm(request.POST)
        if form.is_valid():
            shippingsample = form.save(commit=False)
            shippingsample.order = order
            shippingsample.save()
            data['form_is_valid'] = True
            qs = order.shippingsamples.all().order_by('-created_date')
            data['html_ss_list'] = render_to_string('ss_list.html', {'qs': qs})
        else:
            data['form_is_valid'] = False
    else:
        form = OrdershippingsampleForm()
    context = {'form': form, 'pk': pk}
    data['html_form'] = render_to_string('ss_create_form.html',
                                         context,
                                         request=request)
    data['pk'] = pk
    return JsonResponse(data)


# 船头板进度删除
def ssdelete(request, pk):
    data = dict()
    ss = get_object_or_404(Order_shipping_sample, pk=pk)
    order = ss.order
    pk = order.pk
    ss.delete()
    qs = order.shippingsamples.all().order_by('-created_date')
    data['form_is_valid'] = True
    data['html_ss_list'] = render_to_string('ss_list.html', {'qs': qs})
    data['pk'] = pk
    return JsonResponse(data)


# 船头板进度修改
def ssedit(request, pk):
    data = dict()
    ss = get_object_or_404(Order_shipping_sample, pk=pk)
    order = ss.order
    pk = order.pk
    if request.method == 'POST':
        form = OrdershippingsampleForm(request.POST, instance=ss)
        if form.is_valid():
            form.save()
            qs = order.shippingsamples.all().order_by('-created_date')
            data['form_is_valid'] = True
            data['html_ss_list'] = render_to_string('ss_list.html', {'qs': qs})
        else:
            data['form_is_valid'] = False
    else:
        form = OrdershippingsampleForm(instance=ss)
    context = {'form': form, 'pk': ss.pk}
    data['html_form'] = render_to_string('ss_edit_form.html',
                                         context,
                                         request=request)
    data['pk'] = pk
    return JsonResponse(data)


def progessplist(request, type):
    loginuser = request.user
    # 有问题的大货布进度记录对应的订单列表['orderid']
    bulk_fabric_p = Order_bulk_fabric.objects.filter(status="WARNING").values_list('order', flat=True)
    # 有大货布问题的订单
    orders_bulk_fabric_p = Order.objects.filter(pk__in=bulk_fabric_p)
    # 有问题的生产办进度记录对应的订单列表['orderid']
    fitting_p = Order_fitting_sample.objects.filter(status="WARNING").values_list('order', flat=True)
    # 有生产板问题的订单
    orders_fitting_p = Order.objects.filter(pk__in=fitting_p)
    # 有问题的船头板进度记录对应的订单列表['orderid']
    shipping_p = Order_shipping_sample.objects.filter(status="WARNING").values_list('order', flat=True)
    # 有船头板问题的订单
    orders_shipping_p = Order.objects.filter(pk__in=shipping_p)
    if type == 'fitting':
        if loginuser.is_factory:
            orders = orders_fitting_p.filter(factory=loginuser.factory)
        elif loginuser.is_merchandiser:
            orders = orders_fitting_p.filter(merchandiser=loginuser.merchandiser)
        else:
            orders = orders_fitting_p
        return render(request, 'order_list.html', {'orders': orders})

    elif type == 'bulkfabric':
        if loginuser.is_factory:
            orders = orders_bulk_fabric_p.filter(factory=loginuser.factory)
        elif loginuser.is_merchandiser:
            orders = orders_bulk_fabric_p.filter(merchandiser=loginuser.merchandiser)
        else:
            orders = orders_bulk_fabric_p
        return render(request, 'order_list.html', {'orders': orders})

    else:
        if loginuser.is_factory:
            orders = orders_shipping_p.filter(factory=loginuser.factory)
        elif loginuser.is_merchandiser:
            orders = orders_shipping_p.filter(merchandiser=loginuser.merchandiser)
        else:
            orders = orders_shipping_p
        return render(request, 'order_list.html', {'orders': orders})


class FunctionList(TemplateView):
    template_name = 'function_list.html'
