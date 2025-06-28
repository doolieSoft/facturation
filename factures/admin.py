from django.contrib import admin

from factures.models import LigneFacture, Facture


class LigneFactureInline(admin.TabularInline):
    model = LigneFacture
    extra = 1

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'date']
    inlines = [LigneFactureInline]