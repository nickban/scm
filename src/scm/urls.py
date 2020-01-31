from django.urls import path, include
from . import views

urlpatterns = [
    # 入口链接按角色分类
    path('', views.home.as_view(), name='home'),

    # 样板地址导航
    path('sample/', include(([
        path('', views.SampleList.as_view(), name='samplelist'),
        path('add/step1/', views.SampleAddStep1.as_view(), name='sampleaddstep1'),
        path('add/<int:pk>/step2/', views.SampleAddStep2.as_view(), name='sampleaddstep2'),
        path('<int:pk>/', views.SampleEdit.as_view(), name='sampleedit'),
        path('<int:pk>/osavatar/add/', views.sampleosavataradd, name='sampleosavataradd'),
        path('<int:pk>/detail/', views.SampleDetail.as_view(), name='sampledetail'),
        path('<int:pk>/delete/', views.SampleDelete.as_view(), name='sampledelete'),
        path('<int:pk>/os_pic/<int:sample_ospic_pk>/delete/', views.SampleospicDelete.as_view(), name='sampleospicdelete'),
        path('<int:pk>/pic/<int:sample_pic_pk>/delete/', views.SamplepicDelete.as_view(), name='samplepicdelete'),
        path('<int:pk>/sizespec/<int:sample_sizespec_pk>/delete/', views.SamplesizespecDelete.as_view(), name='samplesizespecdelete'),
        path('<int:pk>/sizespec/add/', views.samplesizespecadd, name='samplesizespecadd'),
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
