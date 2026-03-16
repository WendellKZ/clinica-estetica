from django.urls import path
from . import views

app_name = "servicos"

urlpatterns = [
    path("", views.servico_lista, name="servico_lista"),
    path("novo/", views.servico_novo, name="servico_novo"),
    path("<int:pk>/editar/", views.servico_editar, name="servico_editar"),
    path("<int:pk>/excluir/", views.servico_excluir, name="servico_excluir"),
    path("<int:pk>/toggle/", views.servico_toggle_ativo, name="servico_toggle_ativo"),

    # mantém a rota já existente
    path("sincronizar/", views.sincronizar_servicos, name="sincronizar_servicos"),
]
