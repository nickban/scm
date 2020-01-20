from django.urls import path, include
from . import views

urlpatterns = [
    # 入口链接按角色分类
    path('', views.home, name='home'),

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
]
