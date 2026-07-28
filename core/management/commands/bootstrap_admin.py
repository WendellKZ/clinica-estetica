import os
import secrets

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cria o primeiro administrador de forma idempotente."

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("BOOTSTRAP_ADMIN skipped: superuser already exists")
            return

        username = os.getenv("INITIAL_ADMIN_USERNAME", "admin").strip() or "admin"
        email = os.getenv("INITIAL_ADMIN_EMAIL", "admin@example.com").strip()
        password = os.getenv("INITIAL_ADMIN_PASSWORD", "").strip()
        generated_password = not password
        if generated_password:
            password = secrets.token_urlsafe(18)

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"BOOTSTRAP_ADMIN created username={username}"))
        if generated_password:
            self.stdout.write(
                self.style.WARNING(
                    f"INITIAL_ADMIN_CREDENTIALS username={username} password={password}"
                )
            )
