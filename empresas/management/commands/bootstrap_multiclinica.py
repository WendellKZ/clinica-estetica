from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction

from empresas.utils import ensure_default_empresa

class Command(BaseCommand):
    help = "Cria empresa padrão e preenche o campo empresa em registros existentes (quando houver)."

    @transaction.atomic
    def handle(self, *args, **options):
        emp = ensure_default_empresa()
        self.stdout.write(self.style.SUCCESS(f"Empresa padrão: {emp.nome} (id={emp.id})"))

        targets = [
            ("clientes", "Cliente"),
            ("agenda", "Servico"),
            ("agenda", "Agendamento"),
            ("loja", "Produto"),
            ("loja", "Venda"),
            ("financeiro", "LancamentoFinanceiro"),
        ]

        for app_label, model_name in targets:
            Model = apps.get_model(app_label, model_name)
            if not hasattr(Model, "empresa_id"):
                self.stdout.write(self.style.WARNING(f"{app_label}.{model_name} sem campo empresa (ignore)."))
                continue

            qs = Model.objects.filter(empresa__isnull=True)
            count = qs.count()
            if count:
                qs.update(empresa=emp)
                self.stdout.write(self.style.SUCCESS(f"{app_label}.{model_name}: {count} registro(s) vinculados."))
            else:
                self.stdout.write(f"{app_label}.{model_name}: ok.")

        self.stdout.write(self.style.SUCCESS("Bootstrap multi-clínica concluído."))
