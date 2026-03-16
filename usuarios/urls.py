from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.usuario_lista, name="usuario_lista"),
    path("novo/", views.usuario_novo, name="usuario_novo"),
    path("<int:user_id>/editar/", views.usuario_editar, name="usuario_editar"),
    path("<int:user_id>/toggle-ativo/", views.usuario_toggle_ativo, name="usuario_toggle_ativo"),
    path("<int:user_id>/reset-senha/", views.usuario_reset_senha, name="usuario_reset_senha"),
]
