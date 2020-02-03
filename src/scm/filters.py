from .models import Sample
import django_filters


class SampleFilter(django_filters.FilterSet):
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
            return samples.filter(factory=loginuser.factory)
        else:
            return samples.all()
