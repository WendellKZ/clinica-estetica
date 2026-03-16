from django.core.management.base import BaseCommand
from django.utils import timezone
from django.apps import apps
from decimal import Decimal


class Command(BaseCommand):
    help = "Finaliza automaticamente agendamentos realizados cujo horário já terminou e gera financeiro."

    def handle(self, *args, **options):
        Agendamento = apps.get_model("agenda", "Agendamento")
        Lancamento = None

        # tenta localizar model financeiro se existir
        try:
            Lancamento = apps.get_model("financeiro", "Lancamento")
        except Exception:
            self.stdout.write(self.style.WARNING("Model financeiro.Lancamento não encontrado. Apenas status será atualizado."))

        agora = timezone.now()
        total_finalizados = 0

        agendamentos = Agendamento.objects.filter(status__iexact="Realizado")

        for ag in agendamentos:
            if hasattr(ag, "fim") and ag.fim and ag.fim < agora:

                # evita duplicação se já estiver finalizado
                if ag.status.lower() == "finalizado":
                    continue

                ag.status = "Finalizado"
                ag.save(update_fields=["status"])
                total_finalizados += 1

                # gerar financeiro se existir model
                if Lancamento and hasattr(ag, "servico") and ag.servico:
                    # evita duplicação por referência
                    existe = Lancamento.objects.filter(
                        referencia_id=ag.id,
                        referencia_tipo="agendamento"
                    ).exists()

                    if not existe:
                        Lancamento.objects.create(
                            descricao=f"Serviço: {getattr(ag.servico, 'nome', 'Serviço')}",
                            valor=Decimal(getattr(ag.servico, "preco", 0)),
                            tipo="Receita",
                            referencia_id=ag.id,
                            referencia_tipo="agendamento"
                        )

        self.stdout.write(self.style.SUCCESS(
            f"{total_finalizados} agendamentos finalizados automaticamente."
        ))
