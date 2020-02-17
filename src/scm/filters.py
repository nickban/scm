from scm.models import Order
import django_filters


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['po', 'style_no']

    def __init__(self, *args, **kwargs):
        super(OrderFilter, self).__init__(*args, **kwargs)
        if self.data == {}:
            self.queryset = self.queryset.none()
