# factures/urls.py

from django.urls import path
from .views import FactureCreateView, FactureDetailView, FactureAjouterPrestationView, FactureListView, generer_pdf

urlpatterns = [
    path("<int:pk>/", FactureDetailView.as_view(), name="facture_detail"),
    path("ajouter/", FactureCreateView.as_view(), name="facture_create"),
    path("ajouter-prestation/", FactureAjouterPrestationView.as_view(), name="facture_ajouter_prestation"),  # <== ici

]

urlpatterns += [
    path("", FactureListView.as_view(), name="facture_list"),
    path("<int:pk>/pdf/", generer_pdf, name="generer_pdf")
]
