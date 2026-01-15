from django.contrib import admin
from .models import Produto, Venda, VendaItem

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "sku", "custo", "preco_venda", "estoque_atual", "ativo")
    search_fields = ("nome", "sku")
    list_filter = ("ativo",)

class VendaItemInline(admin.TabularInline):
    model = VendaItem
    extra = 0

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ("id", "data", "cliente", "forma_pagamento", "total", "custo_total")
    inlines = [VendaItemInline]
