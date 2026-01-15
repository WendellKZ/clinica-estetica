from django import forms
from .models import LancamentoFinanceiro

class LancamentoForm(forms.ModelForm):
    class Meta:
        model = LancamentoFinanceiro
        fields = ["tipo", "origem", "data", "valor", "categoria", "descricao"]
        widgets = {"data": forms.DateInput(attrs={"type": "date"})}
