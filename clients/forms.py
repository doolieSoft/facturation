from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["nom", "tva", "adresse", "telephone", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
