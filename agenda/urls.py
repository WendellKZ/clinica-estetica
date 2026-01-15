from django.urls import path
from . import views

urlpatterns = [
    path("", views.agenda_semana, name="agenda_lista"),
    path("dia/", views.agenda_dia, name="agenda_dia"),
    path("novo/", views.agendamento_novo, name="agenda_novo"),
    path("<int:pk>/status/<str:status>/", views.agendamento_mudar_status, name="agenda_status"),
]
