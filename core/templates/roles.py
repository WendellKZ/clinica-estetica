from django import template

register = template.Library()

@register.filter(name="has_group")
def has_group(user, group_name: str) -> bool:
    try:
        if not user or not user.is_authenticated:
            return False
        return user.groups.filter(name=group_name).exists()
    except Exception:
        return False

@register.filter(name="is_admin_user")
def is_admin_user(user) -> bool:
    try:
        return bool(user and user.is_authenticated and user.is_superuser)
    except Exception:
        return False

@register.simple_tag
def can_access_backoffice(user) -> bool:
    """Clientes/Financeiro/Loja."""
    try:
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=["Recepcao"]).exists()
    except Exception:
        return False
