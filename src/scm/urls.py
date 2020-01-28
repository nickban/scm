from django.urls import path, include
from . import views

urlpatterns = [
    # 入口链接按角色分类
    path('', views.home.as_view(), name='home'),

    # 样板地址导航
    path('sample/', include(([
        path('', views.SampleList.as_view(), name='sample_list'),
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
        path('list/', views.PostList.as_view(), name='postlist'),
        path('add/', views.PostAdd.as_view(), name='postadd'),
        path('<int:pk>/', views.PostEdit.as_view(), name='postedit'),
        path('<int:pk>/detail/', views.PostDetail.as_view(), name='postdetail'),
        path('<int:pk>/attach/', views.postattach, name='postattach'),
        path('<int:pk>/attach/<int:postattach_pk>/delete/', views.PostAttachDelete.as_view(), name='postattachdelete'),
        path('<int:pk>/delete/', views.PostDelete.as_view(), name='postdelete'),
    ], 'scm'), namespace='post')),
]
