from django.urls import path

from devis.views import (ConvertirDevisEnFactureView,
                         DevisCreateView,
                         DevisAjouterPrestationView,
                         DevisDetailView,
                         DevisListView, update_devis_envoye)

urlpatterns = [
    path("<int:pk>/", DevisDetailView.as_view(), name="devis_detail"),
    path("ajouter/", DevisCreateView.as_view(), name="devis_create"),
    path("ajouter-prestation/", DevisAjouterPrestationView.as_view(), name="devis_ajouter_prestation"),  # <== ici
]

urlpatterns += [
    path("", DevisListView.as_view(), name="devis_list"),
    path('devis/<int:devis_id>/update_envoye/', update_devis_envoye, name='update_devis_envoye'),
]

urlpatterns += [
    path('devis/<int:devis_id>/convertir/', ConvertirDevisEnFactureView.as_view(), name='convertir_devis_en_facture'),
]
