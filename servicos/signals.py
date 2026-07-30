from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from agenda.models import Servico as ServicoAgenda
from .models import Servico as ServicoPainel


def sincronizar_servico(instance: ServicoPainel) -> ServicoAgenda:
    """Mantém o serviço operacional da agenda igual ao cadastro do painel."""
    nome = (instance.nome or "").strip()
    if not nome:
        raise ValueError("O serviço precisa ter um nome para ser sincronizado.")

    servico, _created = ServicoAgenda.objects.update_or_create(
        nome=nome,
        defaults={
            "preco": instance.preco_padrao,
            "duracao_minutos": instance.duracao_min,
            "ativo": instance.ativo,
        },
    )
    return servico


@receiver(post_save, sender=ServicoPainel)
def sync_servico_para_agenda(sender, instance: ServicoPainel, **kwargs):
    sincronizar_servico(instance)


@receiver(post_delete, sender=ServicoPainel)
def desativar_servico_na_agenda(sender, instance: ServicoPainel, **kwargs):
    ServicoAgenda.objects.filter(nome=(instance.nome or "").strip()).update(ativo=False)
