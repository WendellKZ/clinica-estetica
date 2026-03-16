from __future__ import annotations

from datetime import timedelta

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.http import Http404, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone


def _get_model(app_label: str, model_name: str):
    try:
        return apps.get_model(app_label, model_name)
    except Exception:
        return None


def _get_form():
    """Tenta usar o AgendamentoForm existente; se não existir, cria um ModelForm."""
    try:
        from .forms import AgendamentoForm  # type: ignore
        return AgendamentoForm
    except Exception:
        Agendamento = _get_model("agenda", "Agendamento")
        if not Agendamento:
            raise Http404("Model Agendamento não encontrado.")
        return modelform_factory(Agendamento, exclude=())


def _week_bounds(base_date):
    weekday = base_date.weekday()  # 0=Mon
    start = base_date - timedelta(days=weekday)
    end = start + timedelta(days=6)
    return start, end


@login_required
def agenda_semana(request):
    """Agenda semanal em cards — sempre mostra os 7 dias."""
    try:
        offset = int(request.GET.get("offset", "0"))
    except Exception:
        offset = 0

    today = timezone.localdate()
    base = today + timedelta(weeks=offset)
    semana_inicio, semana_fim = _week_bounds(base)

    Agendamento = _get_model("agenda", "Agendamento")
    ags = []
    if Agendamento:
        qs = Agendamento.objects.all()
        if hasattr(Agendamento, "inicio"):
            start_dt = timezone.make_aware(
                timezone.datetime.combine(semana_inicio, timezone.datetime.min.time())
            )
            end_dt = timezone.make_aware(
                timezone.datetime.combine(semana_fim, timezone.datetime.max.time())
            )
            qs = qs.filter(inicio__range=(start_dt, end_dt)).order_by("inicio")
        elif hasattr(Agendamento, "data"):
            qs = qs.filter(data__range=(semana_inicio, semana_fim)).order_by("data")
        ags = list(qs)

    by_day = {}
    for a in ags:
        if hasattr(a, "inicio") and getattr(a, "inicio", None):
            d = timezone.localtime(a.inicio).date()
        elif hasattr(a, "data") and getattr(a, "data", None):
            d = a.data
        else:
            continue
        by_day.setdefault(d, []).append(a)

    dias = []
    for i in range(7):
        d = semana_inicio + timedelta(days=i)
        dias.append({"grouper": d, "list": by_day.get(d, [])})

    return render(
        request,
        "agenda/agenda.html",
        {
            "dias": dias,
            "semana_inicio": semana_inicio,
            "semana_fim": semana_fim,
            "offset": offset,
        },
    )


# alias compatível com versões anteriores
agenda_lista = agenda_semana


@login_required
def agenda_novo(request):
    """Cria um novo agendamento (compatível com urls.py)."""
    Form = _get_form()
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Agendamento criado com sucesso.")
            return redirect(reverse("agenda:agenda_lista"))
        messages.error(request, "Revise os campos do agendamento.")
    else:
        initial = {}
        now = timezone.localtime()
        if hasattr(Form, "base_fields"):
            if "inicio" in Form.base_fields:
                initial["inicio"] = now.replace(second=0, microsecond=0)
            if "fim" in Form.base_fields:
                initial["fim"] = (now + timedelta(minutes=60)).replace(second=0, microsecond=0)
        form = Form(initial=initial)

    return render(request, "agenda/agenda_form.html", {"form": form, "titulo": "Novo agendamento"})


@login_required
def agenda_editar(request, pk: int):
    Agendamento = _get_model("agenda", "Agendamento")
    if not Agendamento:
        raise Http404("Model Agendamento não encontrado.")
    obj = get_object_or_404(Agendamento, pk=pk)
    Form = _get_form()

    if request.method == "POST":
        form = Form(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Agendamento atualizado.")
            return redirect(reverse("agenda:agenda_lista"))
        messages.error(request, "Revise os campos do agendamento.")
    else:
        form = Form(instance=obj)

    return render(request, "agenda/agenda_form.html", {"form": form, "titulo": "Editar agendamento", "obj": obj})


@login_required
def agenda_status(request, pk: int):
    """Atualiza status via POST (compatível)."""
    if request.method not in ("POST", "PATCH"):
        return HttpResponseNotAllowed(["POST", "PATCH"])

    Agendamento = _get_model("agenda", "Agendamento")
    if not Agendamento:
        raise Http404("Model Agendamento não encontrado.")
    obj = get_object_or_404(Agendamento, pk=pk)

    new_status = request.POST.get("status") or request.GET.get("status")
    if not new_status:
        return JsonResponse({"ok": False, "error": "status ausente"}, status=400)

    if hasattr(obj, "status"):
        setattr(obj, "status", new_status)
        obj.save(update_fields=["status"])
        return JsonResponse({"ok": True, "status": getattr(obj, "status")})
    return JsonResponse({"ok": False, "error": "campo status não existe"}, status=400)
