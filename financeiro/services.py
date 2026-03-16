from .models import LancamentoFinanceiro

def criar_entrada_procedimento(agendamento):
    exists = LancamentoFinanceiro.objects.filter(tipo="ENTRADA", origem="PROCEDIMENTO", agendamento=agendamento).exists()
    if exists:
        return

    kwargs = {}
    if hasattr(LancamentoFinanceiro, "empresa_id") and getattr(agendamento, "empresa_id", None):
        kwargs["empresa_id"] = agendamento.empresa_id

    LancamentoFinanceiro.objects.create(
        tipo="ENTRADA",
        origem="PROCEDIMENTO",
        data=agendamento.inicio.date(),
        valor=agendamento.servico.preco,
        descricao=f"Procedimento: {agendamento.servico.nome} - Cliente: {agendamento.cliente.nome}",
        categoria="Procedimentos",
        agendamento=agendamento,
        **kwargs
    )

def criar_entrada_venda(venda):
    exists = LancamentoFinanceiro.objects.filter(tipo="ENTRADA", origem="VENDA", venda=venda).exists()
    if exists:
        return

    kwargs = {}
    if hasattr(LancamentoFinanceiro, "empresa_id") and getattr(venda, "empresa_id", None):
        kwargs["empresa_id"] = venda.empresa_id

    LancamentoFinanceiro.objects.create(
        tipo="ENTRADA",
        origem="VENDA",
        data=venda.data.date(),
        valor=venda.total,
        descricao=f"Venda loja #{venda.id}",
        categoria="Vendas",
        venda=venda,
        **kwargs
    )
