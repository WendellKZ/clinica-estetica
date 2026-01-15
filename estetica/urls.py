from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("clientes/", include("clientes.urls")),
    path("agenda/", include("agenda.urls")),
    path("loja/", include("loja.urls")),
    path("financeiro/", include("financeiro.urls")),
]
