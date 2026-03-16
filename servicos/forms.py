from django import forms
from .models import Servico

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ["nome", "duracao_min", "preco_padrao", "custo_padrao", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "duracao_min": forms.NumberInput(attrs={"class": "form-control", "min": "5", "step": "5"}),
            "preco_padrao": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "custo_padrao": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
        }
