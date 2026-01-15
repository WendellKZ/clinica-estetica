from datetime import timedelta
import itertools
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Agendamento, Servico
from .forms import AgendamentoForm

def _is_in_group(user, name: str) -> bool:
    try:
        return user.groups.filter(name=name).exists()
    except Exception:
        return False

def _can_view_all(user) -> bool:
    return user.is_superuser or user.is_staff or _is_in_group(user, "Admin") or _is_in_group(user, "Recepcao")

def _filter_qs_by_role(qs, user):
    if _can_view_all(user):
        return qs
    if _is_in_group(user, "Profissional"):
        return qs.filter(profissional=user)
    return qs.filter(Q(profissional=user) | Q(profissional__isnull=True))

def _get_week_range(ref_date):
    monday = ref_date - timedelta(days=ref_date.weekday())
    start = timezone.make_aware(timezone.datetime(monday.year, monday.month, monday.day, 0, 0, 0))
    end = start + timedelta(days=7)
    return start, end

def _has_conflict(profissional, inicio, fim, exclude_pk=None):
    if not profissional or not inicio or not fim:
        return False
    qs = Agendamento.objects.filter(profissional=profissional, inicio__lt=fim, fim__gt=inicio)
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    return qs.exists()

def _build_prof_color_map(users):
    palette = [
        "#b14bbf", "#6b2b7a", "#ff7aa2", "#f4a3b8",
        "#4c78a8", "#72b7b2", "#54a24b", "#eeca3b",
        "#f58518", "#b279a2", "#9d755d", "#bab0ac",
    ]
    colors = {}
    cyc = itertools.cycle(palette)
    for u in users:
        if u and u.id not in colors:
            colors[u.id] = next(cyc)
    return colors

def _apply_colors(agendamentos, prof_colors):
    for a in agendamentos:
        try:
            a.prof_color = prof_colors.get(a.profissional_id) or "#d0d0d0"
        except Exception:
            a.prof_color = "#d0d0d0"
    return agendamentos

@login_required
def agenda_semana(request):
    today = timezone.localdate()
    start, end = _get_week_range(today)

    prof_id = request.GET.get("prof") or ""
    qs = Agendamento.objects.select_related("cliente", "servico", "profissional").filter(
        inicio__gte=start, inicio__lt=end
    ).order_by("inicio")
    qs = _filter_qs_by_role(qs, request.user)
    if prof_id:
        qs = qs.filter(profissional_id=prof_id)

    User = get_user_model()
    profissionais = User.objects.filter(is_active=True).order_by("username")
    if not _can_view_all(request.user):
        profissionais = profissionais.filter(id=request.user.id)

    prof_colors = _build_prof_color_map(profissionais)
    ags = _apply_colors(list(qs), prof_colors)

    return render(request, "agenda/agenda.html", {
        "agendamentos": ags,
        "week_start": start,
        "week_end": end,
        "profissionais": profissionais,
        "prof_id": str(prof_id),
        "view_mode": "semana",
    })

@login_required
def agenda_dia(request):
    dia_str = request.GET.get("dia")
    try:
        if dia_str:
            dia = timezone.datetime.fromisoformat(dia_str).date()
        else:
            dia = timezone.localdate()
    except Exception:
        dia = timezone.localdate()

    start = timezone.make_aware(timezone.datetime(dia.year, dia.month, dia.day, 0, 0, 0))
    end = start + timedelta(days=1)

    prof_id = request.GET.get("prof") or ""
    qs = Agendamento.objects.select_related("cliente", "servico", "profissional").filter(
        inicio__gte=start, inicio__lt=end
    ).order_by("inicio")
    qs = _filter_qs_by_role(qs, request.user)
    if prof_id:
        qs = qs.filter(profissional_id=prof_id)

    User = get_user_model()
    profissionais = User.objects.filter(is_active=True).order_by("username")
    if not _can_view_all(request.user):
        profissionais = profissionais.filter(id=request.user.id)

    prof_colors = _build_prof_color_map(profissionais)
    ags = _apply_colors(list(qs), prof_colors)

    return render(request, "agenda/dia.html", {
        "agendamentos": ags,
        "dia": dia,
        "profissionais": profissionais,
        "prof_id": str(prof_id),
        "view_mode": "dia",
    })

@login_required
def agendamento_novo(request):
    now = timezone.localtime()
    minute = (now.minute // 15 + 1) * 15
    start = now.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=minute)
    end = start + timedelta(hours=1)

    initial = {"inicio": start, "fim": end, "status": "AGENDADO", "duracao_min":"60"}

    servicos_duracoes = {}
    for s in Servico.objects.all().only("id"):
        dur = getattr(s, "duracao_minutos", None)
        if dur is None:
            dur = getattr(s, "duracao_padrao_min", None)
        if dur is None:
            dur = 60
        try:
            servicos_duracoes[str(s.id)] = int(dur)
        except Exception:
            servicos_duracoes[str(s.id)] = 60

    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            ag = form.save(commit=False)
            ag.cliente = form.get_or_create_cliente()

            action = request.POST.get("action", "")
            if action == "confirmar":
                ag.status = "CONFIRMADO"

            if _is_in_group(request.user, "Profissional") and not _can_view_all(request.user):
                ag.profissional = request.user

            if _has_conflict(ag.profissional, ag.inicio, ag.fim):
                messages.error(request, "Conflito de horário: este profissional já possui um agendamento nesse período.")
                return render(request, "agenda/novo.html", {
                    "form": form,
                    "is_profissional": _is_in_group(request.user, "Profissional") and not _can_view_all(request.user),
                    "servicos_duracoes": servicos_duracoes,
                })

            ag.save()
            messages.success(
                request,
                "Agendamento criado e confirmado com sucesso." if ag.status == "CONFIRMADO" else "Agendamento criado com sucesso."
            )
            return redirect("agenda_lista")
    else:
        form = AgendamentoForm(initial=initial)
        if _is_in_group(request.user, "Profissional") and not _can_view_all(request.user):
            form.fields["profissional"].required = False

    return render(request, "agenda/novo.html", {
        "form": form,
        "is_profissional": _is_in_group(request.user, "Profissional") and not _can_view_all(request.user),
        "servicos_duracoes": servicos_duracoes,
    })

@login_required
@require_POST
def agendamento_mudar_status(request, pk, status):
    ag = get_object_or_404(Agendamento.objects.select_related("cliente", "servico", "profissional"), pk=pk)
    if not _can_view_all(request.user) and ag.profissional_id and ag.profissional_id != request.user.id:
        messages.error(request, "Você não tem permissão para alterar este agendamento.")
        return redirect("agenda_lista")

    status = (status or "").upper()
    allowed = {"AGENDADO", "CONFIRMADO", "REALIZADO", "CANCELADO"}
    if status not in allowed:
        messages.error(request, "Status inválido.")
        return redirect("agenda_lista")

    ag.status = status
    ag.save(update_fields=["status"])

    if status == "REALIZADO":
        from loja.models import Venda
        key = f"agendamento #{ag.id}"
        venda = Venda.objects.filter(cliente=ag.cliente, observacao__icontains=key).order_by("-id").first()
        if not venda:
            field = Venda._meta.get_field("forma_pagamento")
            default_forma = field.choices[0][0] if getattr(field, "choices", None) else "PIX"
            venda = Venda.objects.create(
                cliente=ag.cliente,
                forma_pagamento=default_forma,
                observacao=f"Gerado do agendamento #{ag.id} - {getattr(ag.servico, 'nome', ag.servico)}",
                total=0,
                custo_total=0,
            )
            messages.success(request, f"Atendimento marcado como realizado. Venda criada (#{venda.id}). Adicione os itens e finalize.")
        else:
            messages.info(request, f"Atendimento realizado. Venda já existente (#{venda.id}).")
        return redirect("venda_detalhe", pk=venda.pk)

    messages.success(request, f"Status atualizado para: {status.title()}.")
    return redirect("agenda_lista")
