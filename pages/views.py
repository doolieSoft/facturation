# pages/views.py

from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "pages/index.html"
