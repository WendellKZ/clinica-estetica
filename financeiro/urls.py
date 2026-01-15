from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista, name="financeiro_lista"),
    path("novo/", views.novo, name="financeiro_novo"),
]
