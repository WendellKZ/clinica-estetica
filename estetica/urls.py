from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("clientes/", include("clientes.urls")),
    # Agenda usa namespace "agenda" (necessário para templates com {% url 'agenda:...' %})
    path("agenda/", include(("agenda.urls", "agenda"), namespace="agenda")),
    path("loja/", include("loja.urls")),
    path("financeiro/", include("financeiro.urls")),
    path("usuarios/", include("usuarios.urls")),
    path('servicos/', include('servicos.urls')),
        path("produtos/", include("produtos.urls")),
        path("webhooks/whatsapp/", include("notificacoes.urls")),



]
