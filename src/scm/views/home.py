from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import (TemplateView,
                                  CreateView, ListView, UpdateView, DetailView,
                                  DeleteView)
from scm.models import (User, Post, PostAttachment, Sample, Sample_os_pics,
                     Sample_size_specs, Sample_os_avatar,
                     Sample_swatches, Sample_quotation_form,
                     Sample_pics_factory, Sample_size_spec_factory)
from scm.forms import (SignUpForm, NewpostForm, PostAttachmentForm,
                    NewsampleForm, SampleForm, SamplesizespecsForm,
                    SampleosavatarForm, SampleospicsForm,
                    SampleswatchForm, SamplefpicsForm,
                     SampledetailForm)
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import reverse_lazy
from scm.decorators import office_required, merchandiser_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views import View
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from scm.filters import SampleFilter
from django_filters.views import FilterView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages


@method_decorator([login_required], name='dispatch')
class home(TemplateView):
    template_name = 'home.html'


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')
