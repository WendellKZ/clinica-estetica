from .models import Empresa

DEFAULT_EMPRESA_NOME = "Minha Clinica"


def ensure_default_empresa():
    emp = Empresa.objects.filter(ativo=True).order_by("id").first()
    if emp:
        return emp
    return Empresa.objects.create(nome=DEFAULT_EMPRESA_NOME, ativo=True)


def get_current_empresa(request):
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
