from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProdutoForm
from .models import Produto

@login_required
def produto_list(request):
    q = (request.GET.get("q") or "").strip()
    qs = Produto.objects.all().order_by("nome")
    if q:
        qs = qs.filter(Q(nome__icontains=q) | Q(sku__icontains=q))
    return render(request, "produtos/produto_list.html", {"produtos": qs, "q": q})

@login_required
def produto_create(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto cadastrado com sucesso.")
            return redirect("produtos:produto_list")
    else:
        form = ProdutoForm()
    return render(request, "produtos/produto_form.html", {"form": form, "titulo": "Novo produto"})

@login_required
def produto_update(request, pk: int):
    obj = get_object_or_404(Produto, pk=pk)
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso.")
            return redirect("produtos:produto_list")
    else:
        form = ProdutoForm(instance=obj)
    return render(request, "produtos/produto_form.html", {"form": form, "titulo": "Editar produto"})

@login_required
def produto_delete(request, pk: int):
    obj = get_object_or_404(Produto, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Produto removido com sucesso.")
        return redirect("produtos:produto_list")
    return render(request, "produtos/produto_confirm_delete.html", {"produto": obj})
