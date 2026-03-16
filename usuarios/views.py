from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .forms import UsuarioCreateForm, UsuarioUpdateForm, ResetSenhaForm

def somente_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(somente_admin)
def usuario_lista(request):
    q = (request.GET.get("q") or "").strip()
    usuarios = User.objects.all().order_by("username")
    if q:
        usuarios = usuarios.filter(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q)
        )
    return render(request, "usuarios/usuario_lista.html", {"usuarios": usuarios, "q": q})

@login_required
@user_passes_test(somente_admin)
def usuario_novo(request):
    if request.method == "POST":
        form = UsuarioCreateForm(request.POST)
        if form.is_valid():
            u = form.save()
            messages.success(request, f"Usuário '{u.username}' criado com sucesso.")
            return redirect("usuarios:usuario_lista")
        messages.error(request, "Revise os campos do formulário.")
    else:
        form = UsuarioCreateForm()
    return render(request, "usuarios/usuario_form.html", {"form": form, "modo": "novo"})

@login_required
@user_passes_test(somente_admin)
def usuario_editar(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UsuarioUpdateForm(request.POST, instance=u)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuário '{u.username}' atualizado.")
            return redirect("usuarios:usuario_lista")
        messages.error(request, "Revise os campos do formulário.")
    else:
        form = UsuarioUpdateForm(instance=u)
    return render(request, "usuarios/usuario_form.html", {"form": form, "modo": "editar", "alvo": u})

@login_required
@user_passes_test(somente_admin)
def usuario_toggle_ativo(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if u == request.user:
        messages.warning(request, "Você não pode desativar a si mesmo.")
        return redirect("usuarios:usuario_lista")
    u.is_active = not u.is_active
    u.save(update_fields=["is_active"])
    messages.success(request, f"Usuário '{u.username}' agora está {'ATIVO' if u.is_active else 'INATIVO'}.")
    return redirect("usuarios:usuario_lista")

@login_required
@user_passes_test(somente_admin)
def usuario_reset_senha(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = ResetSenhaForm(request.POST)
        if form.is_valid():
            u.set_password(form.cleaned_data["password"])
            u.save()
            messages.success(request, f"Senha do usuário '{u.username}' alterada.")
            return redirect("usuarios:usuario_lista")
        messages.error(request, "Revise os campos do formulário.")
    else:
        form = ResetSenhaForm()
    return render(request, "usuarios/usuario_reset_senha.html", {"form": form, "alvo": u})
