from django.urls import path
from . import views

app_name = "produtos"

urlpatterns = [
    path("", views.produto_list, name="produto_list"),
    path("novo/", views.produto_create, name="produto_create"),
    path("<int:pk>/editar/", views.produto_update, name="produto_update"),
    path("<int:pk>/excluir/", views.produto_delete, name="produto_delete"),
]
