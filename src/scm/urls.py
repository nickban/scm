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
        # 测试用
        path('<int:pk>/copy/', sample.samplecopy, name='samplecopy'),
    ], 'scm'), namespace='sample')),

    # 订单地址导航
    path('order/', include(([
        # 未确认,已确认,已出货订单列表
        path('new/', order.OrderListNew.as_view(), name='orderlistnew'),
        path('confirmed/', order.OrderListConfrimed.as_view(), name='orderlistconfirmed'),
        path('shipped/', order.OrderListShipped.as_view(), name='orderlistshipped'),
        # 订单新增
        path('add/', order.OrderAdd.as_view(), name='orderadd'),
        # 订单编辑，详情，删除
        path('<int:pk>/', order.OrderEdit.as_view(), name='orderedit'),
        path('<int:pk>/delete/', order.OrderDelete.as_view(), name='orderdelete'),
        path('<int:pk>/detail/', order.orderdetail, name='orderdetail'),
        # 订单颜色数量增删改
        path('<int:pk>/colorqty/add/', order.colorqtyadd, name='colorqtyadd'),
        path('<int:pk>/colorqty/<int:colorqtypk>/', order.colorqtyedit, name='colorqtyedit'),
        path('<int:pk>/colorqty/<int:colorqtypk>/delete/', order.colorqtydelete, name='colorqtydelete'),
        # 订单送工厂，通知工厂
        path('<int:pk>/sentfactory/', order.ordersentfactory, name='ordersentfactory'),
        # 订单确认
        path('<int:pk>/confirm/', order.orderconfirm, name='orderconfirm'),
        # 订单出货
        path('<int:pk>/shipped/', order.ordershipped, name='ordershipped'),
        # 测试用
        path('<int:pk>/copy/', order.ordercopy, name='ordercopy'),
        # 订单进度管理
        path('<int:pk>/progress/', order.progress, name='progress'),
        path('<int:pk>/progress/child/', order.child, name='child'),
        # 生产板进度增删改
        path('<int:pk>/progress/fs/', order.fittingsample, name='fittingsample'),
        path('fs/<int:pk>/delete/', order.fsdelete, name='fsdelete'),
        path('fs/<int:pk>/edit/', order.fsedit, name='fsedit'),
        # 大货布进度增删改
        path('<int:pk>/progress/bf/', order.bulkfabric, name='bulkfabric'),
        path('bf/<int:pk>/delete/', order.bfdelete, name='bfdelete'),
        path('bf/<int:pk>/edit/', order.bfedit, name='bfedit'),
        # 船头板进度增删改
        path('<int:pk>/progress/ss/', order.shippingsample, name='shippingsample'),
        path('ss/<int:pk>/delete/', order.ssdelete, name='ssdelete'),
        path('ss/<int:pk>/edit/', order.ssedit, name='ssedit'),

        # 创建装箱单
        path('<int:pk>/packinglist/add/', order.packinglistadd, name='packinglistadd'),
        # 删除装箱单
        path('<int:pk>/packinglist/<int:plpk>/delete/', order.packinglistdelete, name='packinglistdelete'),
        # 装箱单详情
        path('<int:pk>/packinglist/detail/', order.packinglistdetail, name='packinglistdetail'),
        # 装箱单提交
        path('<int:pk>/packinglist/submit/', order.packinglistsubmit, name='packinglistsubmit'),
        # 装箱单关闭，不能更改
        path('<int:pk>/packinglist/close/', order.packinglistclose, name='packinglistclose'),
        # 装箱单重置
        path('<int:pk>/packinglist/reset/', order.packinglistreset, name='packinglistreset'),
        # 查订单颜色的比列
        path('getratio/', order.getratio, name='getratio'),
        # 装箱单查找, 此功能系统暂不使用，代码可以供未来参考
        path('search/', order.plsearch, name='plsearch'),

        path('invoice/add/', order.invoiceadd, name='invoiceadd'),
        path('invoice/<int:pk>/detail/', order.invoicedetail, name='invoicedetail'),
        path('invoice/<int:pk>/delete/', order.invoicedelete, name='invoicedelete'),
        path('invoice/<int:pk>/pay/', order.invoicepay, name='invoicepay'),
        path('invoice/list/', order.invoicelist, name='invoicelist'),
        path('invoice/<int:pk>/attachadd/', order.invoiceattachadd, name='invoiceattachadd'),
        
        # 订单上传资料通用功能
        path('<int:pk>/<str:attachtype>/add/', order.orderattachadd, name='orderattachadd'),
        path('<int:pk>/<str:attachtype>/collection/', order.orderattachcollection, name='orderattachcollection'),
        path('<int:pk>/<str:attachtype>/<int:attach_pk>/delete/', order.orderattachdelete, name='orderattachdelete'),


    ], 'scm'), namespace='order')),

    # admin地址导航
    path('admin/', include(([
        path('', order.FunctionList.as_view(), name='function_list'),
    ], 'scm'), namespace='admin')),

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
