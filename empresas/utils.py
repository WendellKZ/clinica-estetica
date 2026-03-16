from django.utils.text import slugify
from .models import Empresa, PerfilUsuario

DEFAULT_EMPRESA_NOME = "Minha Clínica"

def ensure_default_empresa():
    emp = Empresa.objects.filter(ativo=True).order_by("id").first()
    if emp:
        return emp
    slug = slugify(DEFAULT_EMPRESA_NOME) or "minha-clinica"
    base = slug
    i = 1
    while Empresa.objects.filter(slug=slug).exists():
        i += 1
        slug = f"{base}-{i}"
    return Empresa.objects.create(nome=DEFAULT_EMPRESA_NOME, slug=slug, ativo=True)

def get_current_empresa(request):
    user = getattr(request, "user", None)
    if user and getattr(user, "is_authenticated", False):
        try:
            perfil = PerfilUsuario.objects.select_related("empresa").get(user=user, ativo=True)
            request.session["empresa_id"] = perfil.empresa_id
            return perfil.empresa
        except Exception:
            pass

    emp_id = None
    try:
        emp_id = request.session.get("empresa_id")
    except Exception:
        emp_id = None

    if emp_id:
        emp = Empresa.objects.filter(id=emp_id, ativo=True).first()
        if emp:
            return emp

    emp = ensure_default_empresa()
    try:
        request.session["empresa_id"] = emp.id
    except Exception:
        pass
    return emp
