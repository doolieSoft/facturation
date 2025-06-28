# factures/forms.py

from django import forms
from django.forms.models import inlineformset_factory
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
