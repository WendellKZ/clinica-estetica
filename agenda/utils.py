from django.utils import timezone
from django.db import transaction

from .models import Agendamento, Atendimento
from financeiro.models import LancamentoFinanceiro


def auto_finalizar_agendamentos() -> int:
    """Finaliza agendamentos cujo horário já passou e gera o financeiro (1x).

    Regras:
    - Se fim <= agora e status em MARCADO/CONFIRMADO => marca como REALIZADO.
    - Se já estiver REALIZADO e não tiver financeiro => gera financeiro.
    - Cria Atendimento (1x) quando REALIZADO.
    Retorna: quantidade de agendamentos processados.
    """
    now = timezone.now()

    qs = Agendamento.objects.filter(fim__lte=now).exclude(status__in=["CANCELADO", "FALTOU"])
    processed = 0

    # Faz em transação para evitar duplicar financeiro em concorrência simples.
    with transaction.atomic():
        for ag in qs.select_related("cliente", "servico"):
            mudou_status = False

            if ag.status in ["MARCADO", "CONFIRMADO"]:
                ag.status = "REALIZADO"
                ag.save(update_fields=["status"])
                mudou_status = True

            if ag.status == "REALIZADO":
                # 1) Garante atendimento
                Atendimento.objects.get_or_create(agendamento=ag, defaults={"observacoes": ""})

                # 2) Garante financeiro (evita duplicar)
                existe = LancamentoFinanceiro.objects.filter(
                    agendamento=ag,
                    origem="PROCEDIMENTO",
                    tipo="ENTRADA",
                ).exists()

                if not existe:
                    LancamentoFinanceiro.objects.create(
                        tipo="ENTRADA",
                        origem="PROCEDIMENTO",
                        data=ag.fim.date(),
                        valor=ag.servico.preco,
                        descricao=f"Procedimento: {ag.servico.nome} - {ag.cliente}",
                        agendamento=ag,
                    )

            if mudou_status:
                processed += 1

    return processed
