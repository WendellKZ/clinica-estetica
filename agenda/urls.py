from django.urls import path

from . import views

app_name = "agenda"

urlpatterns = [
    # visões específicas
    # Compatibilidade: em algumas versões antigas a view "agenda_dia" não existe.
    # Para não quebrar o import do urls.py, mantemos o name="agenda_dia" mas
    # apontamos para a view semanal (que existe no projeto).
    path("dia/", views.agenda_semana, name="agenda_dia"),
    # view real chama-se agenda_novo (mantemos compatibilidade no views.py)
    path("novo/", views.agenda_novo, name="agenda_novo"),

    # editar
    path("<int:pk>/editar/", views.agenda_editar, name="agenda_editar"),

    # navegação semanal por offset (aceita valores negativos: -1, 1, etc.)
    # Mantemos o MESMO name para permitir reverse com/sem parâmetro.
    path("<str:offset>/", views.agenda_semana, name="agenda_lista"),

    # padrão (semana atual)
    path("", views.agenda_semana, name="agenda_lista"),
]
