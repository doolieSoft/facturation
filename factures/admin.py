from django.contrib import admin

from factures.models import LigneFacture, Facture


class LigneFactureInline(admin.TabularInline):
    model = LigneFacture
    extra = 1

class LigneFactureAdmin(admin.ModelAdmin):
    list_display = ("facture", "prestation", "quantite", "prix_unitaire", "cout_unitaire", "marge")
    readonly_fields = ("marge",)

    def marge(self, obj):
        m = obj.marge()
        return f"{m:.2f} €" if m is not None else "-"
    marge.short_description = "Marge (€)"

admin.site.register(LigneFacture, LigneFactureAdmin)

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'date']
    inlines = [LigneFactureInline]
