from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

DEFAULT_ROLE_MATRIX = {
    "ADM": {"all": True},
    "PROFISSIONAL": {"perms": [
        "agenda.view_agendamento",
        "agenda.add_agendamento",
        "agenda.change_agendamento",
    ]},
    "ESTOQUE": {"perms": [
        "produtos.view_produto",
        "produtos.add_produto",
        "produtos.change_produto",
        "produtos.delete_produto",
        "servicos.view_servico",
        "servicos.add_servico",
        "servicos.change_servico",
        "servicos.delete_servico",
    ]},
    "FINANCEIRO": {"perms": [
        "financeiro.view_lancamento",
        "financeiro.add_lancamento",
        "financeiro.change_lancamento",
        "loja.view_venda",
    ]},
}

class Command(BaseCommand):
    help = "Cria/atualiza grupos e permissões padrão."

    def handle(self, *args, **options):
        self._ensure_dashboard_perm()

        for role, cfg in DEFAULT_ROLE_MATRIX.items():
            g, _ = Group.objects.get_or_create(name=role)
            g.permissions.clear()

            if cfg.get("all"):
                g.permissions.set(Permission.objects.all())
                continue

            perm_objs, missing = [], []
            for p in cfg.get("perms", []):
                app_label, codename = p.split(".", 1)
                perm = Permission.objects.filter(content_type__app_label=app_label, codename=codename).first()
                if perm:
                    perm_objs.append(perm)
                else:
                    missing.append(p)

            g.permissions.set(perm_objs)
            if missing:
                self.stdout.write(self.style.WARNING(f"[{role}] Ajuste nomes de permissão: {missing}"))

        self.stdout.write(self.style.SUCCESS("OK: grupos/permissões criados."))
        self.stdout.write("Para liberar Dashboard a alguém, conceda a permissão: core.view_dashboard")

    def _ensure_dashboard_perm(self):
        from core.models_permission import DashboardPermission
        ct = ContentType.objects.get_for_model(DashboardPermission)
        Permission.objects.get_or_create(
            content_type=ct,
            codename="view_dashboard",
            defaults={"name": "Pode ver o Dashboard"},
        )
