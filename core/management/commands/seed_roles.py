from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Cria grupos básicos de acesso: Admin, Recepcao, Profissional"

    def handle(self, *args, **options):
        for name in ["Admin", "Recepcao", "Profissional"]:
            Group.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Grupos criados/confirmados: Admin, Recepcao, Profissional"))
