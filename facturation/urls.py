# facturation/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("pages.urls")),  # page d'accueil
    path("clients/", include("clients.urls")),

    path('prestations/', include('prestations.urls')),
    path('factures/', include('factures.urls')),

]
