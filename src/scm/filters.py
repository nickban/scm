from .models import Sample
import django_filters
from django.db.models import Q


class SampleFilter(django_filters.FilterSet):
    sample_no = django_filters.CharFilter(label='样板号', lookup_expr='contains')
    class Meta:
        model = Sample
        fields = ['sample_no', 'brand', 'designer', 'merchandiser', 'style',
                  'factory', 'status']

    @property
    def qs(self):
        samples = super().qs
        loginuser = getattr(self.request, 'user', None)
        if loginuser.is_merchandiser:
            return samples.filter(merchandiser=loginuser.merchandiser)
        if loginuser.is_factory:
            return samples.filter(Q(factory=loginuser.factory),
                                  Q(status='SENT_F') | Q(status='COMPLETED'))
        else:
            return samples.all()
