from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista, name="clientes_lista"),
    path("novo/", views.novo, name="clientes_novo"),
    path("<int:pk>/editar/", views.editar, name="clientes_editar"),
]
