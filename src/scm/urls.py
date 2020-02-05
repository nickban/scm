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
        path('<int:pk>/<str:attachtype>/collection/', sample.sampleattachcollection, name='sampleattachcollection'),
        path('<int:pk>/<str:attachtype>/<int:attach_pk>/delete/', sample.sampleattachdelete, name='sampleattachdelete'),
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
