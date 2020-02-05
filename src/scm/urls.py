from django.urls import path, include
from .views import order, sample, post, home

urlpatterns = [
    # 入口链接按角色分类
    path('', home.home.as_view(), name='home'),

    # 样板地址导航
    path('sample/', include(([
        # 未完成，已完成样板列表
        path('', sample.SampleListNew.as_view(), name='samplelistnew'),
        path('completed/', sample.SampleListCompleted.as_view(), name='samplelistcompleted'),
        # 样板新增
        path('add/step1/', sample.SampleAddStep1.as_view(), name='sampleaddstep1'),
        path('add/<int:pk>/step2/', sample.SampleAddStep2.as_view(), name='sampleaddstep2'),
        # 样板编辑，详情，删除
        path('<int:pk>/', sample.SampleEdit.as_view(), name='sampleedit'),
        path('<int:pk>/detail/', sample.SampleDetail.as_view(), name='sampledetail'),
        path('<int:pk>/delete/', sample.SampleDelete.as_view(), name='sampledelete'),
        # 样板上传资料通用功能
        path('<int:pk>/<str:attachtype>/add/', sample.sampleattachadd, name='sampleattachadd'),
        # path('<int:pk>/<str:type>/collection/<str:preurl>/', sample.SampleattachCollection.as_view(), name='sampleattachcollection'),
        # path('<int:pk>/<str:type>/<int:attach_pk>/delete/<str:preurl>/', sample.SampleattachDelete.as_view(), name='sampleattachdelete'),


        # 样板款式图
        # path('<int:pk>/osavatar/add/', sample.sampleosavataradd, name='sampleosavataradd'),
        path('<int:pk>/osavatar/<int:sample_osavatar_pk>/delete/', sample.SampleosavatarDelete.as_view(), name='sampleosavatardelete'),
        # 样板原板照片
        path('<int:pk>/os_pics/add/', sample.sampleospicadd, name='sampleospicadd'),
        path('<int:pk>/os_pics/collection/<str:preurl>/', sample.SampleospicsCollection.as_view(), name='sampleospicscollection'),
        path('<int:pk>/os_pics/<int:sample_ospic_pk>/delete/<str:preurl>/', sample.SampleospicDelete.as_view(), name='sampleospicdelete'),
        # 样板客人尺寸表
        path('<int:pk>/sizespecs/<int:sample_sizespec_pk>/delete/', sample.SamplesizespecDelete.as_view(), name='samplesizespecdelete'),
        path('<int:pk>/sizespecs/add/', sample.samplesizespecadd, name='samplesizespecadd'),
        # 样板色卡
        path('<int:pk>/swatch/add/', sample.sampleswatchadd, name='sampleswatchadd'),
        path('<int:pk>/swatch/collection/', sample.SampleswatchCollection.as_view(), name='sampleswatchcollection'),
        path('<int:pk>/swatch/<int:sample_swatch_pk>/delete/', sample.SampleswatchDelete.as_view(), name='sampleswatchdelete'),
        # 样板完成照片
        path('<int:pk>/fpics/add/', sample.samplefpicsadd, name='samplefpicsadd'),
        path('<int:pk>/fpics/collection/', sample.SamplefpicsCollection.as_view(), name='samplefpicscollection'),
        path('<int:pk>/fpics/<int:sample_fpic_pk>/delete/', sample.SamplefpicDelete.as_view(), name='samplefpicdelete'),
        # 样板报价单
        path('<int:pk>/quotation/add/', sample.samplequotationadd, name='samplequotationadd'),
        path('<int:pk>/quotation/<int:sample_quotation_pk>/delete/', sample.SamplequotationDelete.as_view(), name='samplequotationdelete'),
        # 样板成样尺寸表
        path('<int:pk>/sizespecf/add/', sample.samplesizespecfadd, name='samplesizespecfadd'),
        path('<int:pk>/sizespecf/<int:sample_sizespecf_pk>/delete/', sample.SamplesizespecfDelete.as_view(), name='samplesizespecfdelete'),
        # 样板送工厂，通知工厂
        path('<int:pk>/sentfactory/', sample.samplesentfactory, name='samplesentfactory'),
        # 样板已完成
        path('<int:pk>/completed/', sample.samplecompleted, name='samplecompleted'),
    ], 'scm'), namespace='sample')),

    # 订单地址导航
    path('order/', include(([
        path('', order.OrderList.as_view(), name='order_list'),
    ], 'scm'), namespace='order')),

    # admin地址导航
    path('admin/', include(([
        path('', order.FunctionList.as_view(), name='function_list'),
    ], 'scm'), namespace='admin')),

    # Finance地址导航
    path('finance/', include(([
        path('', order.InvoiceList.as_view(), name='invoice_list'),
    ], 'scm'), namespace='finance')),

    # post地址导航
    path('post/', include(([
        path('', post.PostList.as_view(), name='postlist'),
        path('add/', post.PostAdd.as_view(), name='postadd'),
        path('<int:pk>/', post.PostEdit.as_view(), name='postedit'),
        path('<int:pk>/detail/', post.PostDetail.as_view(), name='postdetail'),
        path('<int:pk>/attach/add/', post.postattach, name='postattach'),
        path('<int:pk>/attach/<int:postattach_pk>/delete/', post.PostAttachDelete.as_view(), name='postattachdelete'),
        path('<int:pk>/delete/', post.PostDelete.as_view(), name='postdelete'),
    ], 'scm'), namespace='post')),
]
