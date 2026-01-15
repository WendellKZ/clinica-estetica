from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils import timezone

@login_required
def dashboard(request):
    # 🔒 Apenas ADMIN (superuser) pode ver o Dashboard
    if not request.user.is_superuser:
        messages.error(request, "Acesso restrito: apenas o usuário Admin pode visualizar o Dashboard.")
        return redirect("agenda_lista")

    # Se o seu dashboard original tinha mais cálculos, eles continuam no template via outras views/apps.
    hoje = timezone.localdate()
    return render(request, "dashboard.html", {"hoje": hoje})

def login_view(request):
    # Se já está logado, manda para o lugar certo
    if request.user.is_authenticated:
        # Admin cai no dashboard, demais caem na agenda
        return redirect("dashboard" if request.user.is_superuser else "agenda_lista")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("dashboard" if user.is_superuser else "agenda_lista")
        messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "login.html", {"form": form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("login")
