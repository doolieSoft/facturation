# core/forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Prestation

class PrestationForm(forms.ModelForm):
    class Meta:
        model = Prestation
        fields = ["description", "prix", "tva"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
