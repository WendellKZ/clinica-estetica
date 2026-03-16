from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PerfilUsuario
from .utils import ensure_default_empresa

User = get_user_model()

@receiver(post_save, sender=User)
def criar_perfil_padrao(sender, instance, created, **kwargs):
    if not created:
        return
    if PerfilUsuario.objects.filter(user=instance).exists():
        return
    empresa = ensure_default_empresa()
    papel = "ADMIN" if instance.is_superuser else "RECEPCAO"
    PerfilUsuario.objects.create(user=instance, empresa=empresa, papel=papel, ativo=True)
