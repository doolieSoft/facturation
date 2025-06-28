from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["nom", "numero_tva", "email", "telephone"]
    search_fields = ["nom", "numero_tva", "email"]
