from django.apps import AppConfig

class ServicosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "servicos"
    verbose_name = "Serviços (Painel)"

    def ready(self):
        # Garante que, ao criar/editar serviços no painel, eles também apareçam
        # na Agenda (que usa o modelo de Serviço do app agenda).
        try:
            from . import signals  # noqa: F401
        except Exception:
            # Evita quebrar o start do Django caso haja migrações pendentes
            # ou o app agenda ainda não esteja carregado.
            pass
