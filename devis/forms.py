from django import forms
from .models import Devis, LigneDevis
from django.forms import inlineformset_factory

class DevisForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = ['client', 'remarques']

LigneDevisFormSet = inlineformset_factory(
    Devis, LigneDevis,
    fields=['prestation', 'quantite', 'prix_unitaire', 'cout_unitaire', 'tva'],
    extra=1, can_delete=True
)
