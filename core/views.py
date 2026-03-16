from django.contrib.auth.decorators import login_required
from django.db.utils import OperationalError, ProgrammingError
from django.shortcuts import render

from agenda.models import Agendamento
from clientes.models import Cliente
from loja.models import Venda


from django.utils.timezone import now
from datetime import date
from django.db.models import Sum

@login_required
def dashboard(request):
    """
    Dashboard principal.
    """
    from financeiro.models import LancamentoFinanceiro
    from loja.models import Produto
    from loja.models import Venda

    hoje_date = now().date()
    primeiro_dia_mes = hoje_date.replace(day=1)

    # Filtrar lançamentos em geral
    qs_fin = LancamentoFinanceiro.objects.all()
    if hasattr(LancamentoFinanceiro, 'empresa_id') and getattr(request, 'empresa', None):
        qs_fin = qs_fin.filter(empresa=request.empresa)

    # Cálculos Hoje
    qs_hoje = qs_fin.filter(data=hoje_date)
    entradas_hoje = qs_hoje.filter(tipo='ENTRADA').aggregate(t=Sum('valor'))['t'] or 0
    saidas_hoje = qs_hoje.filter(tipo='SAIDA').aggregate(t=Sum('valor'))['t'] or 0
    
    # Custo Produtos Hoje (das vendas de hoje)
    qs_vendas = Venda.objects.filter(data__date=hoje_date)
    if hasattr(Venda, 'empresa_id') and getattr(request, 'empresa', None):
         qs_vendas = qs_vendas.filter(empresa=request.empresa)
    custo_hoje = qs_vendas.aggregate(t=Sum('custo_total'))['t'] or 0
    lucro_hoje = entradas_hoje - (saidas_hoje + custo_hoje)

    hoje = {
        'entradas': f"{entradas_hoje:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        'saidas_totais': f"{(saidas_hoje + custo_hoje):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        'lucro_real': f"{lucro_hoje:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    }

    # Cálculos Mês
    qs_mes = qs_fin.filter(data__gte=primeiro_dia_mes)
    entradas_mes = qs_mes.filter(tipo='ENTRADA').aggregate(t=Sum('valor'))['t'] or 0
    saidas_mes = qs_mes.filter(tipo='SAIDA').aggregate(t=Sum('valor'))['t'] or 0
    
    qs_vendas_mes = Venda.objects.filter(data__date__gte=primeiro_dia_mes)
    if hasattr(Venda, 'empresa_id') and getattr(request, 'empresa', None):
         qs_vendas_mes = qs_vendas_mes.filter(empresa=request.empresa)
    custo_mes = qs_vendas_mes.aggregate(t=Sum('custo_total'))['t'] or 0
    lucro_mes = entradas_mes - (saidas_mes + custo_mes)

    mes = {
        'entradas': f"{entradas_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        'saidas_totais': f"{(saidas_mes + custo_mes):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        'lucro_real': f"{lucro_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    }

    clientes_count = Cliente.objects.filter(empresa=request.empresa).count() if hasattr(Cliente, 'empresa_id') and getattr(request, 'empresa', None) else Cliente.objects.count()
    produtos_count = Produto.objects.filter(empresa=request.empresa).count() if hasattr(Produto, 'empresa_id') and getattr(request, 'empresa', None) else Produto.objects.count()

    context = {
        "hoje": hoje,
        "mes": mes,
        "clientes_count": clientes_count,
        "produtos_count": produtos_count,
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
        from django.template import engines
        html = """
        <h2>Login</h2>
        <form method='post'>
            {% csrf_token %}
            <input type='text' name='username' placeholder='Usuário'/> <br/><br/>
            <input type='password' name='password' placeholder='Senha'/> <br/><br/>
            <button type='submit'>Entrar</button>
        </form>
        """
        django_engine = engines['django']
        template = django_engine.from_string(html)
        return HttpResponse(template.render({}, request))
