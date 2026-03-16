from .utils import auto_finalizar_agendamentos


class AutoFinalizarAgendamentosMiddleware:
    """Middleware leve: ao acessar o sistema, finaliza automaticamente agendamentos vencidos.

    Vantagens:
    - Sem Celery/cron (baixo custo).
    - Garante que, ao abrir o sistema, tudo fica atualizado.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Só roda para usuários logados (evita custo em páginas públicas)
        try:
            if getattr(request, "user", None) is not None and request.user.is_authenticated:
                auto_finalizar_agendamentos()
        except Exception:
            # Nunca derruba o site por causa do job automático.
            pass

        return self.get_response(request)
