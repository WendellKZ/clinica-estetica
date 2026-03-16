from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils import timezone

from .models import Agendamento


@staff_member_required
def agenda_grade(request):
    """Visão em grade por profissional (um dia). GET ?data=YYYY-MM-DD"""
    data_str = (request.GET.get("data") or "").strip()
    if data_str:
        try:
            dia = datetime.strptime(data_str, "%Y-%m-%d").date()
        except Exception:
            dia = timezone.localdate()
    else:
        dia = timezone.localdate()

    ags = (
        Agendamento.objects
        .select_related("profissional", "cliente", "servico")
        .filter(inicio__date=dia)
        .order_by("inicio")
    )

    profissionais = []
    seen = set()
    for a in ags:
        if a.profissional_id and a.profissional_id not in seen:
            profissionais.append(a.profissional)
            seen.add(a.profissional_id)

    return render(
        request,
        "agenda/grade.html",
        {"dia": dia, "profissionais": profissionais, "agendamentos": ags},
    )
