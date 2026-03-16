from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse


def login_view(request):
    """Login simples com fallback (não depende de template)."""
    if request.user.is_authenticated:
        try:
            return redirect("dashboard")
        except Exception:
            return redirect("/")

    if request.method == "POST":
        username = (request.POST.get("username") or request.POST.get("usuario") or "").strip()
        password = request.POST.get("password") or request.POST.get("senha") or ""

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                return redirect("dashboard")
            except Exception:
                return redirect("/")

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


def logout_view(request):
    """Logout e redireciona para a tela de login."""
    logout(request)
    try:
        return redirect("login")
    except Exception:
        return redirect(reverse("login"))
