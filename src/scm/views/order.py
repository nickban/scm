from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from scm.models import (Order,)
from scm.forms import (
                       NeworderForm,)
from django.contrib.auth.decorators import login_required
from scm.decorators import o_m_mg_or_required, o_m_mg_f_or_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import reverse_lazy
from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import messages

# 订单列表-未确认(新建，已送工厂状态)
@method_decorator([login_required, o_m_mg_f_or_required], name='dispatch')
class OrderListNew(ListView):
    model = Order
    ordering = ('-created_date', )
    context_object_name = 'orders'
    template_name = 'order_list.html'

    def get_queryset(self):
        loginuser = self.request.user
        if loginuser.is_merchandiser:
            return Order.objects.filter(Q(merchandiser=loginuser.merchandiser),
                                        Q(status='NEW') | Q(status='SENT_F')).order_by('-created_date')
        elif loginuser.is_factory:
            return Order.objects.filter(factory=loginuser.factory, status='SENT_F').order_by('-created_date')
        else:
            return Order.objects.filter(Q(status='NEW') | Q(status='SENT_F')).order_by('-created_date')

# 订单列表-已确认(已确认状态)
@method_decorator([login_required, o_m_mg_f_or_required], name='dispatch')
class OrderListConfrimed(ListView):
    model = Order
    ordering = ('-created_date', )
    context_object_name = 'orders'
    template_name = 'order_list.html'

    def get_queryset(self):
        loginuser = self.request.user
        if loginuser.is_merchandiser:
            return Order.objects.filter(Q(merchandiser=loginuser.merchandiser),
                                        Q(status='COMFIRMED'))
        elif loginuser.is_factory:
            return Order.objects.filter(Q(factory=loginuser.factory),
                                        Q(status='COMFIRMED'))
        else:
            return Order.objects.filter(status='COMFIRMED')


# 订单列表-已出货(已出货状态)
@method_decorator([login_required, o_m_mg_f_or_required], name='dispatch')
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

# 订单新建
@method_decorator([login_required, o_m_mg_or_required], name='dispatch')
class OrderAdd(CreateView):
    model = Order
    form_class = NeworderForm
    template_name = 'order_edit.html'

    def form_valid(self, form):
        order = form.save()
        messages.success(self.request, '订单创建成功!')
        return redirect('order:orderedit', pk=order.pk)

# # 样板更新
# @method_decorator([login_required, o_m_mg_or_required], name='dispatch')
# class SampleEdit(UpdateView):
#     model = Sample
#     form_class = SampleForm
#     template_name = 'sample_edit.html'
#     context_object_name = 'sample'

#     def get_context_data(self, **kwargs):
#         kwargs['os_pics'] = self.get_object().os_pics.all()
#         kwargs['size_specs'] = self.get_object().size_specs.all()
#         kwargs['swatches'] = self.get_object().swatches.all()
#         kwargs['fpics'] = self.get_object().factory_pics.all()
#         try:
#             kwargs['os_avatar'] = self.get_object().os_avatar
#         except ObjectDoesNotExist:
#             kwargs['os_avatar'] = ''
#         try:
#             kwargs['quotation'] = self.get_object().quotation
#         except ObjectDoesNotExist:
#             kwargs['quotation'] = ''
#         try:
#             kwargs['sizespecf'] = self.get_object().sizespecf
#         except ObjectDoesNotExist:
#             kwargs['sizespecf'] = ''
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         sample = form.save()
#         return redirect('sample:sampleedit', pk=sample.pk)


# # 改变样板状态到送工厂状态
# @o_m_mg_or_required
# def samplesentfactory(request, pk):
#     sample = get_object_or_404(Sample, pk=pk)
#     if sample.factory is None:
#         messages.warning(request, '请选择工厂并保存后，才能通知工厂!')
#     else:
#         sample.status = "SENT_F"
#         sample.save()
#         messages.success(request, '样板已经安排给工厂，并已邮件通知!')
#     return redirect('sample:sampleedit', pk=sample.pk)


# # 改变样板状态到已完成状态
# @o_m_mg_or_required
# def samplecompleted(request, pk):
#     sample = get_object_or_404(Sample, pk=pk)
#     sample.status = "COMPLETED"
#     sample.save()
#     messages.success(request, '样板已完成, 请在已完成列表查找!')
#     return redirect('sample:sampleedit', pk=sample.pk)


# # 工厂查看样板详情页，部分信息，报价单，色卡，成样照片，成样尺寸表
# @method_decorator([login_required, o_m_mg_f_or_required], name='dispatch')
# class SampleDetail(UpdateView):
#     template_name = 'sample_detail.html'
#     model = Sample
#     form_class = SampledetailForm
#     context_object_name = 'sample'

#     def form_valid(self, form):
#         sample = form.save()
#         return redirect('sample:sampledetail', pk=sample.pk)

#     def get_context_data(self, **kwargs):
#         kwargs['os_pics'] = self.get_object().os_pics.all()
#         kwargs['size_specs'] = self.get_object().size_specs.all()
#         kwargs['swatches'] = self.get_object().swatches.all()
#         kwargs['fpics'] = self.get_object().factory_pics.all()
#         try:
#             kwargs['quotation'] = self.get_object().quotation
#         except ObjectDoesNotExist:
#             kwargs['quotation'] = ''
#         try:
#             kwargs['sizespecf'] = self.get_object().sizespecf
#         except ObjectDoesNotExist:
#             kwargs['sizespecf'] = ''
#         return super().get_context_data(**kwargs)


# # 拷贝样板，测试数据用
# def samplecopy(request, pk):
#     sample = get_object_or_404(Sample, pk=pk)
#     sample.pk = None
#     sample.save()
#     return redirect('sample:sampleedit', pk=sample.pk)


# # 删除样板
# @method_decorator([login_required, o_m_mg_or_required], name='dispatch')
# class SampleDelete(DeleteView):
#     model = Sample
#     context_object_name = 'sample'
#     template_name = 'sample_delete.html'
#     success_url = reverse_lazy('sample:samplelistnew')


# # 样板附件通用功能视图
# @login_required
# def sampleattachadd(request, pk, attachtype):
#     sample = get_object_or_404(Sample, pk=pk)
#     previous_url = request.META.get('HTTP_REFERER')
#     if attachtype == 'osavatar':
#         if request.FILES:
#             try:
#                 sample.os_avatar.delete()
#             except ObjectDoesNotExist:
#                 pass
#             form = SampleosavatarForm(request.POST, request.FILES)
#     elif attachtype == 'os_pics':
#         form = SampleospicsForm(request.POST, request.FILES)
#     elif attachtype == 'sizespecs':
#         form = SamplesizespecsForm(request.POST, request.FILES)
#     elif attachtype == 'swatch':
#         form = SampleswatchForm(request.POST, request.FILES)
#     elif attachtype == 'fpics':
#         form = SamplefpicsForm(request.POST, request.FILES)
#     elif attachtype == 'quotation':
#         if request.FILES:
#             try:
#                 sample.quotation.delete()
#             except ObjectDoesNotExist:
#                 pass
#             form = SamplequotationForm(request.POST, request.FILES)
#     else:
#         if request.FILES:
#             try:
#                 sample.sizespecf.delete()
#             except ObjectDoesNotExist:
#                 pass
#             form = SamplesizespecfForm(request.POST, request.FILES)
#     if request.method == 'POST':
#         if form.is_valid():
#             with transaction.atomic():
#                 attach = form.save(commit=False)
#                 attach.sample = sample
#                 attach.save()
#                 data = {"files": [{
#                             "name": attach.file.name,
#                             "url": attach.file.url, },
#                             ]}
#         else:
#             data = {'is_valid': False}
#         return JsonResponse(data)
#     else:
#         return render(request, 'sample_attach_add.html', {'sample': sample, 'previous_url': previous_url, 'attachtype': attachtype})


# @login_required
# def sampleattachdelete(request, pk, attachtype, attach_pk):
#     sample = get_object_or_404(Sample, pk=pk)
#     previous_url = request.META.get('HTTP_REFERER')
#     attachtype = attachtype
#     if attachtype == 'osavatar':
#         attach = get_object_or_404(Sample_os_avatar, pk=attach_pk)
#         attach.delete()
#         if 'step2' in previous_url:
#             return redirect('sample:sampleaddstep2', pk=sample.pk)
#         else:
#             return redirect('sample:sampleedit', pk=sample.pk)
#     elif attachtype == 'os_pics':
#         attach = get_object_or_404(Sample_os_pics, pk=attach_pk)
#         attach.delete()
#         return redirect('sample:sampleattachcollection', pk=sample.pk, attachtype=attachtype)
#     elif attachtype == 'sizespecs':
#         attach = get_object_or_404(Sample_size_specs, pk=attach_pk)
#         attach.delete()
#         if 'step2' in previous_url:
#             return redirect('sample:sampleaddstep2', pk=sample.pk)
#         else:
#             return redirect('sample:sampleedit', pk=sample.pk)
#     elif attachtype == 'swatch':
#         attach = get_object_or_404(Sample_swatches, pk=attach_pk)
#         attach.delete()
#         return redirect('sample:sampleattachcollection', pk=sample.pk, attachtype=attachtype)

#         return redirect('sample:sampleattachcollection', pk=sample.pk, attachtype=attachtype)
#     elif attachtype == 'fpics':
#         attach = get_object_or_404(Sample_pics_factory, pk=attach_pk)
#         attach.delete()
#         return redirect('sample:sampleattachcollection', pk=sample.pk, attachtype=attachtype)

#     elif attachtype == 'quotation':
#         attach = get_object_or_404(Sample_quotation_form, pk=attach_pk)
#         attach.delete()
#         if request.user.is_factory:
#             return redirect('sample:sampledetail', pk=sample.pk)
#         else:
#             return redirect('sample:sampleedit', pk=sample.pk)
#     else:
#         attach = get_object_or_404(Sample_size_spec_factory, pk=attach_pk)
#         attach.delete()
#         if request.user.is_factory:
#             return redirect('sample:sampledetail', pk=sample.pk)
#         else:
#             return redirect('sample:sampleedit', pk=sample.pk)


# @login_required
# def sampleattachcollection(request, pk, attachtype):
#     sample = get_object_or_404(Sample, pk=pk)
#     previous_url = request.META.get('HTTP_REFERER')
#     attachtype = attachtype
#     if attachtype == 'os_pics':
#         attaches = sample.os_pics.all()
#     elif attachtype == 'swatch':
#         attaches = sample.swatches.all()
#     elif attachtype == 'fpics':
#         attaches = sample.factory_pics.all()
#     else:
#         attaches = sample.size_specs.all()
#     return render(request, 'sample_attach_collection.html', {'sample': sample,
#                   'attachtype': attachtype, 'attaches': attaches, 'previous_url': previous_url})



class FunctionList(TemplateView):
    template_name = 'function_list.html'


class InvoiceList(TemplateView):
    template_name = 'invoice_list.html'