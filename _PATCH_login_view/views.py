from django.contrib.auth.decorators import login_required
from django.db.utils import OperationalError, ProgrammingError
from django.shortcuts import render

from agenda.models import Agendamento
from clientes.models import Cliente
from loja.models import Venda


@login_required
def dashboard(request):
    """Dashboard principal.

    Quando estamos migrando para Multi-clínica, pode existir o app `empresas`.
    Se as migrations ainda não foram aplicadas, o Django pode estourar
    `OperationalError: no such table: empresas_empresa`.

    Este dashboard fica resiliente: se faltar a tabela, ele carrega e mostra um
    aviso para rodar as migrations.
    """

    total_clientes = Cliente.objects.count()
    total_agendamentos = Agendamento.objects.count()
    total_vendas = Venda.objects.count()

    empresa = None
    precisa_migrar_empresas = False

    try:
        from empresas.models import Empresa
        try:
            empresa = Empresa.objects.first()
        except (OperationalError, ProgrammingError):
            precisa_migrar_empresas = True
    except ModuleNotFoundError:
        # App ainda não foi adicionado
        empresa = None

    context = {
        "total_clientes": total_clientes,
        "total_agendamentos": total_agendamentos,
        "total_vendas": total_vendas,
        "empresa": empresa,
        "precisa_migrar_empresas": precisa_migrar_empresas,
    }
    return render(request, "dashboard.html", context)

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.http import HttpResponse

def login_view(request):
    """
    View de login do sistema.
    - GET: mostra a tela de login (se existir template) ou fallback simples.
    - POST: autentica e redireciona.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = (request.POST.get("username") or request.POST.get("usuario") or "").strip()
        password = request.POST.get("password") or request.POST.get("senha") or ""

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return HttpResponse("Login inválido. Volte e tente novamente.", status=401)

    try:
        return render(request, "core/login.html")
    except Exception:
        return HttpResponse(
            "<h2>Login</h2>"
            "<form method='post'>"
            "<input type='text' name='username' placeholder='Usuário'/> <br/><br/>"
            "<input type='password' name='password' placeholder='Senha'/> <br/><br/>"
            "<button type='submit'>Entrar</button>"
            "</form>"
        )
