from django.contrib import messages
from django.shortcuts import redirect

def user_in_groups(user, groups):
    try:
        return user.is_authenticated and user.groups.filter(name__in=list(groups)).exists()
    except Exception:
        return False

def is_admin(user):
    return bool(user and user.is_authenticated and user.is_superuser)

def can_backoffice(user):
    """Clientes/Financeiro/Loja."""
    return is_admin(user) or user_in_groups(user, ["Recepcao"])

def deny(request, msg="Acesso restrito.", redirect_name="agenda_lista"):
    messages.error(request, msg)
    return redirect(redirect_name)
