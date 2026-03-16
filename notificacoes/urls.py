from django.urls import path
from . import views

urlpatterns = [
    path("", views.webhook, name="whatsapp_webhook_verify"),
    path("events/", views.webhook_events, name="whatsapp_webhook_events"),
]
