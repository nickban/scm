from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from django.shortcuts import render
from django.db.models import F, Sum, DecimalField, ExpressionWrapper,  Q
from scm.models import Order

class ProfitView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'chart.html')

class ProfitViewData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        dataall = []
        dataau = []
        datanz = []
        datasg = []
        datakr = []
        for month in range(1,13):
            # 全部订单，状态已出货
            ordersall = Order.objects.filter(Q(status="SHIPPED"), Q(handover_date_f__month=month))
            ordersall = ordersall.annotate(profit=ExpressionWrapper(
                        (F('disigner_price')-F('factory_price'))*F('actual_ship_qty'), 
                        output_field=DecimalField()))
            profit= ordersall.aggregate(profittotal=Sum('profit', output_field=DecimalField()))
            profit_number = profit['profittotal']
            dataall.append(profit_number)
            # 澳洲 订单
            orderau = Order.objects.filter(Q(status="SHIPPED"), Q(handover_date_f__month=month), Q(destination='AU'))
            orderau = orderau.annotate(profit=ExpressionWrapper(
                       (F('disigner_price')-F('factory_price'))*F('actual_ship_qty'), 
                       output_field=DecimalField()))
            profit= orderau.aggregate(profittotal=Sum('profit', output_field=DecimalField()))
            profit_number = profit['profittotal']
            dataau.append(profit_number)

            # NZ 订单
            ordersnz = Order.objects.filter(Q(status="SHIPPED"), Q(handover_date_f__month=month), Q(destination='NZ'))
            ordersnz = ordersnz.annotate(profit=ExpressionWrapper(
                         (F('disigner_price')-F('factory_price'))*F('actual_ship_qty'), 
                         output_field=DecimalField()))
            profit= ordersnz.aggregate(profittotal=Sum('profit', output_field=DecimalField()))
            profit_number = profit['profittotal']
            datanz.append(profit_number)

            # SG 订单
            orderssg = Order.objects.filter(Q(status="SHIPPED"), Q(handover_date_f__month=month), Q(destination='SG'))
            orderssg = orderssg.annotate(profit=ExpressionWrapper(
                         (F('disigner_price')-F('factory_price'))*F('actual_ship_qty'), 
                         output_field=DecimalField()))
            profit= orderssg.aggregate(profittotal=Sum('profit', output_field=DecimalField()))
            profit_number = profit['profittotal']
            datasg.append(profit_number)

            # 韩国 订单
            orderskr = Order.objects.filter(Q(status="SHIPPED"), Q(handover_date_f__month=month), Q(destination='KR'))
            orderskr = orderskr.annotate(profit=ExpressionWrapper(
                       (F('disigner_price')-F('factory_price'))*F('actual_ship_qty'), 
                       output_field=DecimalField()))
            profit= orderskr.aggregate(profittotal=Sum('profit', output_field=DecimalField()))
            profit_number = profit['profittotal']
            datakr.append(profit_number)


        data = {
            "labels": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
            "dataall": dataall,
            "dataau": dataau,
            "datanz": datanz,
            "datasg": datasg,
            "datakr": datakr,
        }   

        return Response(data)