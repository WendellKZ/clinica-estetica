from django.urls import path
from . import views

urlpatterns = [
    path("", views.loja_home, name="loja_home"),
path("produtos/", views.produtos, name="produtos_lista"),
    path("produtos/novo/", views.produto_novo, name="produto_novo"),
    path("produtos/<int:pk>/editar/", views.produto_editar, name="produto_editar"),

    path("vendas/nova/", views.venda_nova, name="venda_nova"),
    path("vendas/<int:pk>/", views.venda_detalhe, name="venda_detalhe"),
    path("vendas/<int:pk>/finalizar/", views.venda_finalizar, name="venda_finalizar"),
]
