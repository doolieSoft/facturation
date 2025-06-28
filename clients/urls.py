from django.urls import path
from .views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView

urlpatterns = [
    path("", ClientListView.as_view(), name="client_list"),
    path("ajouter/", ClientCreateView.as_view(), name="client_create"),
    path("<int:pk>/modifier/", ClientUpdateView.as_view(), name="client_update"),
    path("<int:pk>/supprimer/", ClientDeleteView.as_view(), name="client_delete"),
]
