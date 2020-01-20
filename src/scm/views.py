from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .forms import MyAuthenticationForm

class HomeView(TemplateView):
    template_name = 'home.html'

