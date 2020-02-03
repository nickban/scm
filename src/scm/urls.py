from django.urls import path, include
from . import views
from . import utils

urlpatterns = [
    # 入口链接按角色分类
    path('', views.home.as_view(), name='home'),

    # 样板地址导航
    path('sample/', include(([
        path('', views.SampleList.as_view(), name='samplelist'),
        # 样板新增
        path('add/step1/', views.SampleAddStep1.as_view(), name='sampleaddstep1'),
        path('add/<int:pk>/step2/', views.SampleAddStep2.as_view(), name='sampleaddstep2'),
        # 样板编辑，详情，删除
        path('<int:pk>/', views.SampleEdit.as_view(), name='sampleedit'),
        path('<int:pk>/detail/', views.SampleDetail.as_view(), name='sampledetail'),
        path('<int:pk>/delete/', views.SampleDelete.as_view(), name='sampledelete'),
        # 样板款式图
        path('<int:pk>/osavatar/add/', views.sampleosavataradd, name='sampleosavataradd'),
        path('<int:pk>/osavatar/<int:sample_osavatar_pk>/delete/', views.SampleosavatarDelete.as_view(), name='sampleosavatardelete'),
        # 样板原板照片
        path('<int:pk>/os_pics/add/', views.sampleospicadd, name='sampleospicadd'),
        path('<int:pk>/os_pics/collection/<str:preurl>/', views.SampleospicsCollection.as_view(), name='sampleospicscollection'),
        path('<int:pk>/os_pics/<int:sample_ospic_pk>/delete/<str:preurl>/', views.SampleospicDelete.as_view(), name='sampleospicdelete'),
        # 样板起板尺寸表
        path('<int:pk>/sizespecs/<int:sample_sizespec_pk>/delete/', views.SamplesizespecDelete.as_view(), name='samplesizespecdelete'),
        path('<int:pk>/sizespecs/add/', views.samplesizespecadd, name='samplesizespecadd'),
        # 样板色卡
        path('<int:pk>/swatch/add/', views.sampleswatchadd, name='sampleswatchadd'),
        path('<int:pk>/swatch/collection/', views.SampleswatchCollection.as_view(), name='sampleswatchcollection'),
        path('<int:pk>/swatch/<int:sample_swatch_pk>/delete/', views.SampleswatchDelete.as_view(), name='sampleswatchdelete'),
        # 样板完成照片
        path('<int:pk>/fpics/add/', views.samplefpicsadd, name='samplefpicsadd'),
        path('<int:pk>/fpics/collection/', views.SamplefpicsCollection.as_view(), name='samplefpicscollection'),
        path('<int:pk>/fpics/<int:sample_fpic_pk>/delete/', views.SamplefpicDelete.as_view(), name='samplefpicdelete'),

        # 样板报价单
        path('<int:pk>/quotation/add/', views.samplequotationadd, name='samplequotationadd'),
        path('<int:pk>/quotation/<int:sample_quotation_pk>/delete/', views.SamplequotationDelete.as_view(), name='samplequotationdelete'),

        # 样板成样尺寸表
        path('<int:pk>/sizespecf/add/', views.samplesizespecfadd, name='samplesizespecfadd'),
        path('<int:pk>/sizespecf/<int:sample_sizespecf_pk>/delete/', views.SamplesizespecfDelete.as_view(), name='samplesizespecfdelete'),

        # 样板打印
        # path('<int:pk>/pdf/', utils.generate_pdf, name='generatepdf'),
        path('<int:pk>/print/', views.sampledetailprint, name='sampledetailprint'),

        # 样板上一个下一个
        # path('<int:pk>/next/', views.samplenext, name='samplenext'),

        # 样板查找
        path('search/', views.samplesearch.as_view(), name='samplesearch'),

    ], 'scm'), namespace='sample')),

    # 订单地址导航
    path('order/', include(([
        path('', views.OrderList.as_view(), name='order_list'),
    ], 'scm'), namespace='order')),

    # admin地址导航
    path('admin/', include(([
        path('', views.FunctionList.as_view(), name='function_list'),
    ], 'scm'), namespace='admin')),

    # Finance地址导航
    path('finance/', include(([
        path('', views.InvoiceList.as_view(), name='invoice_list'),
    ], 'scm'), namespace='finance')),

    # post地址导航
    path('post/', include(([
        path('', views.PostList.as_view(), name='postlist'),
        path('add/', views.PostAdd.as_view(), name='postadd'),
        path('<int:pk>/', views.PostEdit.as_view(), name='postedit'),
        path('<int:pk>/detail/', views.PostDetail.as_view(), name='postdetail'),
        path('<int:pk>/attach/add/', views.postattach, name='postattach'),
        path('<int:pk>/attach/<int:postattach_pk>/delete/', views.PostAttachDelete.as_view(), name='postattachdelete'),
        path('<int:pk>/delete/', views.PostDelete.as_view(), name='postdelete'),
    ], 'scm'), namespace='post')),
]
