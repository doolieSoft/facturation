# core/urls.py

from django.urls import path
from .views import (
    PrestationListView,
    PrestationCreateView,
    PrestationUpdateView,
    PrestationDeleteView,
    PrestationCreatePartialView,
    PrestationCreateAjaxView,
)

urlpatterns = [
    path("", PrestationListView.as_view(), name="prestation_list"),
    path("ajouter/", PrestationCreateView.as_view(), name="prestation_create"),
    path("<int:pk>/modifier/", PrestationUpdateView.as_view(), name="prestation_update"),
    path("<int:pk>/supprimer/", PrestationDeleteView.as_view(), name="prestation_delete"),
]

urlpatterns += [
    path("ajax/ajouter-formulaire/", PrestationCreatePartialView.as_view(), name="prestation_form_partial"),
    path("ajax/ajouter/", PrestationCreateAjaxView.as_view(), name="prestation_create_ajax"),
]