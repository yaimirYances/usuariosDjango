import datetime
from django.shortcuts import render
from django.views.generic import TemplateView

class FechaMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fecha"] = datetime.datetime.now()
        return context

class HomePage(FechaMixin, TemplateView):
    template_name = "home/index.html"

class TempleteFechaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"
