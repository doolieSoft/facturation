# facturation/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("clients/", include("clients.urls")),
                  path('prestations/', include('prestations.urls')),
                  path('factures/', include('factures.urls')),
                  path('devis/', include('devis.urls')),
                  path("", include("pages.urls")),  # page d'accueil

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
