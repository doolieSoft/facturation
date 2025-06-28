# core/views.py
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Prestation

from .forms import PrestationForm


class PrestationCreatePartialView(CreateView):
    model = Prestation
    form_class = PrestationForm
    template_name = "prestations/partials/prestation_form_partial.html"

class PrestationCreateAjaxView(CreateView):
    model = Prestation
    form_class = PrestationForm

    def form_valid(self, form):
        prestation = form.save()
        options_html = render_to_string("prestations/partials/prestation_options.html", {
            "prestations": Prestation.objects.all()
        })
        return HttpResponse(options_html)

class PrestationCreateView(CreateView):
    model = Prestation
    form_class = PrestationForm
    template_name = "prestations/prestation_form.html"
    success_url = reverse_lazy("prestation_list")


class PrestationUpdateView(UpdateView):
    model = Prestation
    form_class = PrestationForm
    template_name = "prestations/prestation_form.html"
    success_url = reverse_lazy("prestation_list")


class PrestationListView(ListView):
    model = Prestation
    template_name = "prestations/prestation_list.html"
    context_object_name = "prestations"


class PrestationDeleteView(DeleteView):
    model = Prestation
    template_name = "prestations/prestation_confirm_delete.html"
    success_url = reverse_lazy("prestation_list")
