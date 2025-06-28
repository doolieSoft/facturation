# factures/forms.py

from django import forms
from django.forms.models import inlineformset_factory

from prestations.models import Prestation
from .models import Facture, LigneFacture


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['client']


LigneFactureFormSet = inlineformset_factory(
    Facture,
    LigneFacture,
    fields=['prestation', 'quantite'],
    extra=1,
    can_delete=True
)


class LigneFactureForm(forms.ModelForm):
    class Meta:
        model = LigneFacture
        fields = ['prestation', 'quantite', 'prix_unitaire', 'cout_unitaire']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si instance nouvelle (pas encore sauvegardée) : préremplir prix et coût
        if not self.instance.pk:
            prestation_id = self.initial.get('prestation') or self.data.get('prestation')
            if prestation_id:
                try:
                    prestation = Prestation.objects.get(pk=prestation_id)
                    self.fields['prix_unitaire'].initial = prestation.prix
                    self.fields['cout_unitaire'].initial = prestation.prix  # par défaut même que prix
                except Prestation.DoesNotExist:
                    pass
