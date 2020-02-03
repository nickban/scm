from .models import Sample
import django_filters


class SampleFilter(django_filters.FilterSet):
    class Meta:
        model = Sample
        fields = ['sample_no', 'brand', 'designer', 'merchandiser', 'style',
                  'factory', 'status']
        
