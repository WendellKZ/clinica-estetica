from django.contrib import admin
from .models import Servico, Agendamento, Atendimento, AtendimentoProduto

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "duracao_minutos")
    search_fields = ("nome",)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ("inicio", "cliente", "servico", "profissional", "status")
    list_filter = ("status", "profissional")
    search_fields = ("cliente__nome", "servico__nome")

class AtendimentoProdutoInline(admin.TabularInline):
    model = AtendimentoProduto
    extra = 0

@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ("agendamento", "created_at")
    inlines = [AtendimentoProdutoInline]
