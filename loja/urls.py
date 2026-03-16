from django.urls import path
from . import views

app_name = "loja"

urlpatterns = [
    path("", views.loja_home, name="loja_home"),

    # Rotas padrão (singular)
    path("venda/nova/", views.venda_nova, name="venda_nova"),
    path("venda/<int:pk>/", views.venda_detalhe, name="venda_detalhe"),
    path("venda/<int:pk>/finalizar/", views.venda_finalizar, name="venda_finalizar"),

    # Aliases (plural) para não quebrar links antigos / menu
    path("vendas/nova/", views.venda_nova, name="vendas_nova"),
    path("vendas/<int:pk>/", views.venda_detalhe, name="vendas_detalhe"),
    path("vendas/<int:pk>/finalizar/", views.venda_finalizar, name="vendas_finalizar"),

    # Produtos dentro da Loja
    path("produtos/", views.produtos_lista, name="produtos_lista"),
    path("produtos/novo/", views.produto_novo, name="produto_novo"),
    path("produtos/<int:pk>/editar/", views.produto_editar, name="produto_editar"),

    # JSON para autofill (preço/custo)
    path("produtos/<int:pk>/json/", views.produto_json, name="produto_json"),
]
