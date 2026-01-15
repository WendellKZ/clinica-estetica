from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import LancamentoFinanceiro
from .forms import LancamentoForm
from loja.models import VendaItem
from agenda.models import AtendimentoProduto

def _custo_produtos(start, end):
    venda_custo = (VendaItem.objects.filter(venda__data__date__gte=start, venda__data__date__lte=end)
                   .aggregate(total=Sum("custo_total"))["total"] or 0)
    atend_custo = (AtendimentoProduto.objects.filter(atendimento__created_at__date__gte=start, atendimento__created_at__date__lte=end)
                   .aggregate(total=Sum("custo_total"))["total"] or 0)
    return venda_custo + atend_custo

@login_required
def lista(request):
    # filtros por período
    inicio = request.GET.get("inicio")
    fim = request.GET.get("fim")
    if not inicio:
        inicio = date.today().replace(day=1).isoformat()
    if not fim:
        fim = date.today().isoformat()

    qs = LancamentoFinanceiro.objects.filter(data__gte=inicio, data__lte=fim).order_by("-data", "-id")
    entradas = qs.filter(tipo="ENTRADA").aggregate(total=Sum("valor"))["total"] or 0
    saidas = qs.filter(tipo="SAIDA").aggregate(total=Sum("valor"))["total"] or 0
    custo = _custo_produtos(date.fromisoformat(inicio), date.fromisoformat(fim))
    lucro_real = entradas - saidas - custo

    return render(request, "financeiro/lista.html", {
        "lancamentos": qs,
        "inicio": inicio, "fim": fim,
        "entradas": entradas, "saidas": saidas, "custo": custo, "lucro_real": lucro_real
    })

@login_required
def novo(request):
    if request.method == "POST":
        form = LancamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("financeiro_lista")
    else:
        form = LancamentoForm()
    return render(request, "financeiro/form.html", {"form": form})
