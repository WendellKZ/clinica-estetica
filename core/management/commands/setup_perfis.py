from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

GROUPS = {
    "Recepcao": {
        "apps": ["agenda", "clientes", "loja", "financeiro"],
        "perms": ["view", "add", "change"],  # sem delete por segurança
    },
    "Profissional": {
        "apps": ["agenda"],
        "perms": ["view", "change"],  # pode mudar status / confirmar, etc.
    },
}

class Command(BaseCommand):
    help = "Cria grupos de acesso (Recepcao, Profissional) e atribui permissões padrão."

    def handle(self, *args, **options):
        for group_name, cfg in GROUPS.items():
            group, _ = Group.objects.get_or_create(name=group_name)

            # limpa e reaplica para ficar idempotente
            group.permissions.clear()

            apps = cfg.get("apps", [])
            perms = cfg.get("perms", [])

            qs = Permission.objects.none()
            for app_label in apps:
                for p in perms:
                    qs = qs | Permission.objects.filter(content_type__app_label=app_label, codename__startswith=p + "_")

            qs = qs.distinct()
            group.permissions.add(*qs)

            self.stdout.write(self.style.SUCCESS(
                f"Grupo '{group_name}' pronto: {qs.count()} permissões atribuídas."
            ))

        self.stdout.write(self.style.WARNING(
            "Próximo passo: no Django Admin, edite usuários e coloque-os nos grupos Recepcao ou Profissional."
        ))
