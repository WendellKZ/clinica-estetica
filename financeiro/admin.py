from django.contrib import admin
from .models import LancamentoFinanceiro

@admin.register(LancamentoFinanceiro)
class LancamentoFinanceiroAdmin(admin.ModelAdmin):
    list_display = ("data", "tipo", "origem", "valor", "categoria", "descricao")
    list_filter = ("tipo", "origem", "categoria")
    search_fields = ("descricao",)
