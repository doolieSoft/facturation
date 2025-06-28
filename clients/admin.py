from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["nom", "tva", "email", "telephone"]
    search_fields = ["nom", "tva", "email"]
