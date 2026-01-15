from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.shortcuts import render, redirect, get_object_or_404

from .models import Produto, Venda, VendaItem
from .forms import ProdutoForm, VendaForm, AddItemForm
from clientes.models import Cliente
from financeiro.services import criar_entrada_venda

@login_required
def produtos(request):
    qs = Produto.objects.all().order_by("-id")
    return render(request, "loja/produtos.html", {"produtos": qs})

@login_required
def produto_novo(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("produtos_lista")
    else:
        form = ProdutoForm()
    return render(request, "loja/produto_form.html", {"form": form, "titulo": "Novo produto"})

@login_required
def produto_editar(request, pk):
    obj = get_object_or_404(Produto, pk=pk)
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("produtos_lista")
    else:
        form = ProdutoForm(instance=obj)
    return render(request, "loja/produto_form.html", {"form": form, "titulo": f"Editar produto: {obj.nome}"})

def _recalcular_totais(venda: Venda):
    tot = venda.itens.all().aggregate(
        total_sub=models.Sum("subtotal"),
        total_custo=models.Sum("custo_total"),
    )
    venda.total = tot["total_sub"] or Decimal("0")
    venda.custo_total = tot["total_custo"] or Decimal("0")
    venda.save(update_fields=["total", "custo_total"])

@login_required
def venda_nova(request):
    if request.method == "POST":
        f = VendaForm(request.POST)
        if f.is_valid():
            cliente = f.cleaned_data.get("cliente")
            if not cliente:
                nome = (f.cleaned_data.get("cliente_nome") or "").strip()
                if nome:
                    cliente = Cliente.objects.create(
                        nome=nome,
                        telefone=(f.cleaned_data.get("cliente_telefone") or "").strip(),
                        email=(f.cleaned_data.get("cliente_email") or "").strip(),
                    )

            venda = Venda.objects.create(
                cliente=cliente,
                forma_pagamento=f.cleaned_data["forma_pagamento"],
                observacao=f.cleaned_data.get("observacao") or "",
                total=0,
                custo_total=0,
            )
            return redirect("venda_detalhe", pk=venda.pk)
    else:
        f = VendaForm()
    return render(request, "loja/venda_nova.html", {"form": f})

@login_required
def venda_detalhe(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    add_form = AddItemForm(request.POST or None)

    if request.method == "POST" and "add_item" in request.POST:
        if add_form.is_valid():
            produto = add_form.cleaned_data.get("produto")
            qtd = add_form.cleaned_data["quantidade"]

            if produto:
                VendaItem.objects.create(
                    venda=venda,
                    produto=produto,
                    nome_produto="",
                    quantidade=qtd,
                    preco_unitario=produto.preco_venda,
                    custo_unitario=produto.custo,
                )
            else:
                nome = (add_form.cleaned_data.get("item_nome") or "").strip()
                preco = add_form.cleaned_data.get("preco_unitario") or Decimal("0")
                custo = add_form.cleaned_data.get("custo_unitario")
                if custo is None:
                    custo = Decimal("0")
                VendaItem.objects.create(
                    venda=venda,
                    produto=None,
                    nome_produto=nome,
                    quantidade=qtd,
                    preco_unitario=preco,
                    custo_unitario=custo,
                )

            _recalcular_totais(venda)
            messages.success(request, "Item adicionado.")
            return redirect("venda_detalhe", pk=venda.pk)

    return render(request, "loja/venda_detalhe.html", {
        "venda": venda,
        "add_form": add_form,
    })

@login_required
@transaction.atomic
def venda_finalizar(request, pk):
    venda = get_object_or_404(Venda, pk=pk)

    if venda.itens.count() == 0:
        messages.error(request, "Adicione ao menos 1 item antes de finalizar.")
        return redirect("venda_detalhe", pk=venda.pk)

    # baixa estoque só dos itens com produto cadastrado
    for item in venda.itens.select_related("produto").all():
        if item.produto_id:
            p = item.produto
            if p.estoque_atual < item.quantidade:
                messages.error(request, f"Estoque insuficiente para {p.nome}. Estoque: {p.estoque_atual}")
                return redirect("venda_detalhe", pk=venda.pk)
            p.estoque_atual -= item.quantidade
            p.save(update_fields=["estoque_atual"])

    _recalcular_totais(venda)
    criar_entrada_venda(venda)

    messages.success(request, "Venda finalizada e entrada registrada no financeiro.")
    return redirect("venda_detalhe", pk=venda.pk)

@login_required
def loja_home(request):
    # Home da Loja: abre a Nova venda (evita 404 em /loja/)
    return redirect('venda_nova')

