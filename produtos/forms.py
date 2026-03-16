from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "sku", "custo", "preco_venda", "estoque_atual", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "sku": forms.TextInput(attrs={"class": "form-control"}),
            "custo": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "preco_venda": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "estoque_atual": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
