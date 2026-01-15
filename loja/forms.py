from django import forms
from .models import Produto, Venda
from clientes.models import Cliente

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "sku", "custo", "preco_venda", "estoque_atual", "ativo"]

class VendaForm(forms.Form):
    # Cliente: escolher existente OU cadastrar na hora
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
    cliente_nome = forms.CharField(required=False, label="Nome do cliente")
    cliente_telefone = forms.CharField(required=False, label="Telefone")
    cliente_email = forms.EmailField(required=False, label="Email")

    forma_pagamento = forms.ChoiceField(choices=Venda.FORMA_CHOICES)
    observacao = forms.CharField(required=False)

class AddItemForm(forms.Form):
    # 1) produto cadastrado
    produto = forms.ModelChoiceField(queryset=Produto.objects.filter(ativo=True), required=False)
    # 2) item cadastrado na hora
    item_nome = forms.CharField(required=False, label="Produto (nome)")
    quantidade = forms.IntegerField(min_value=1, initial=1)
    preco_unitario = forms.DecimalField(min_value=0, required=False, label="Preço (R$)")
    custo_unitario = forms.DecimalField(min_value=0, required=False, label="Custo (R$)")

    def clean(self):
        data = super().clean()
        produto = data.get("produto")
        nome = (data.get("item_nome") or "").strip()
        preco = data.get("preco_unitario")
        custo = data.get("custo_unitario")

        if not produto and not nome:
            raise forms.ValidationError("Selecione um produto OU informe o nome do produto.")
        if not produto and preco is None:
            raise forms.ValidationError("Informe o preço do item.")
        # ✅ Para manter LUCRO REAL correto, custo vira obrigatório quando não há produto cadastrado
        if not produto and custo is None:
            raise forms.ValidationError("Informe também o custo do item (para manter o lucro real correto).")
        return data
