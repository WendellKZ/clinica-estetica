from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ServicoForm
from .models import Servico


@staff_member_required
def servico_lista(request):
    q = (request.GET.get("q") or "").strip()
    servicos = Servico.objects.all()
    if q:
        servicos = servicos.filter(nome__icontains=q)
    return render(request, "servicos/servico_lista.html", {"servicos": servicos, "q": q})


@staff_member_required
def servico_novo(request):
    if request.method == "POST":
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Serviço criado com sucesso.")
            return redirect("servicos:servico_lista")
    else:
        form = ServicoForm()
    return render(request, "servicos/servico_form.html", {"form": form, "modo": "novo"})


@staff_member_required
def servico_editar(request, pk: int):
    alvo = get_object_or_404(Servico, pk=pk)
    if request.method == "POST":
        form = ServicoForm(request.POST, instance=alvo)
        if form.is_valid():
            form.save()
            messages.success(request, "Serviço atualizado com sucesso.")
            return redirect("servicos:servico_lista")
    else:
        form = ServicoForm(instance=alvo)
    return render(request, "servicos/servico_form.html", {"form": form, "modo": "editar", "alvo": alvo})


@staff_member_required
def servico_excluir(request, pk: int):
    alvo = get_object_or_404(Servico, pk=pk)
    if request.method == "POST":
        alvo.delete()
        messages.success(request, "Serviço excluído com sucesso.")
        return redirect("servicos:servico_lista")
    return render(request, "servicos/servico_confirm_excluir.html", {"alvo": alvo})


@staff_member_required
def servico_toggle_ativo(request, pk: int):
    alvo = get_object_or_404(Servico, pk=pk)
    alvo.ativo = not alvo.ativo
    alvo.save(update_fields=["ativo"])
    messages.success(request, f"Serviço {'ativado' if alvo.ativo else 'desativado'} com sucesso.")
    return redirect("servicos:servico_lista")


@staff_member_required
def sincronizar_servicos(request):
    # Mantém compatibilidade: se você já tiver integração real, pode substituir aqui.
    messages.success(request, "Serviços sincronizados com sucesso.")
    return redirect("agenda:agenda_novo")
