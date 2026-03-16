from .models import Empresa
from .utils import get_current_empresa

def empresa_context(request):
    empresa = getattr(request, "empresa", None) or get_current_empresa(request)
    empresas = Empresa.objects.filter(ativo=True).order_by("nome")
    return {"current_empresa": empresa, "empresas_ativas": empresas}
