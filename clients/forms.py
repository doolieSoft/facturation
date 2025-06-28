from django import forms
from crispy_forms.helper import FormHelper
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["nom", "numero_tva", "rue", "code_postal", "ville", "pays", "telephone", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
