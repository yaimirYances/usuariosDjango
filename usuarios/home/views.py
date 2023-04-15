import datetime
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class FechaMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fecha"] = datetime.datetime.now()
        return context

class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "home/index.html"
    #Deteccion de usuario no logueado
    login_url = reverse_lazy("users_app:user-login")

class TempleteFechaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"
