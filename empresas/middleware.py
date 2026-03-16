from __future__ import annotations

from django.utils.deprecation import MiddlewareMixin

try:
    from .models import Empresa
except Exception:
    Empresa = None  # type: ignore


class EmpresaMiddleware(MiddlewareMixin):
    """
    Middleware base para multi-clínica.
    Define request.empresa (Empresa ativa) para ser usada em views/forms.
    Nesta fase (fundação), escolhe:
      1) Empresa selecionada na sessão (empresa_id), se existir e válida
      2) Senão, a primeira Empresa cadastrada
      3) Senão, None

    "Safe": não quebra o sistema mesmo sem migrações/tabela ainda.
    """

    def process_request(self, request):
        request.empresa = None

        if Empresa is None:
            return None

        try:
            qs = Empresa.objects.all()
        except Exception:
            return None

        empresa_id = request.session.get("empresa_id")
        if empresa_id:
            try:
                request.empresa = qs.get(id=empresa_id)
                return None
            except Exception:
                request.empresa = None

        try:
            request.empresa = qs.order_by("id").first()
        except Exception:
            request.empresa = None

        return None
