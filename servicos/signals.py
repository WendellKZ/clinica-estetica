from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Servico as ServicoPainel


@receiver(post_save, sender=ServicoPainel)
def sync_servico_para_agenda(sender, instance: ServicoPainel, **kwargs):
    """Sincroniza o Serviço criado/atualizado no painel para o app Agenda.

    Motivo: a tela de Novo Agendamento normalmente lista serviços do app `agenda`.
    Em algumas versões, o painel de Serviços foi criado em um app separado (`servicos`),
    então o cadastro não aparecia no dropdown da agenda.

    Estratégia: cria/atualiza um registro equivalente no modelo `agenda.Servico`
    (chave por nome). Mantém campos compatíveis quando existirem.
    """
    try:
        from agenda.models import Servico as ServicoAgenda
    except Exception:
        return

    nome = (instance.nome or "").strip()
    if not nome:
        return

    # Monta defaults de forma defensiva (caso o modelo da agenda tenha campos diferentes)
    defaults = {}

    for campo in ("duracao_min", "preco_padrao", "custo_padrao", "ativo"):
        if hasattr(instance, campo):
            defaults[campo] = getattr(instance, campo)

    # Alguns projetos usam "status" ao invés de "ativo"
    if "ativo" not in defaults and hasattr(instance, "status"):
        defaults["status"] = getattr(instance, "status")

    try:
        ServicoAgenda.objects.update_or_create(nome=nome, defaults=defaults)
    except Exception:
        # Se não houver campo `nome` único ou estrutura diferente, não quebrar o sistema.
        pass
