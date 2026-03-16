from django.contrib import admin
from .models import WhatsAppOutbox, WhatsAppCanal

@admin.register(WhatsAppCanal)
class WhatsAppCanalAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "ativo", "phone_number_id", "waba_id", "criado_em")
    list_filter = ("ativo",)
    search_fields = ("nome", "phone_number_id", "waba_id")

@admin.register(WhatsAppOutbox)
class WhatsAppOutboxAdmin(admin.ModelAdmin):
    list_display = ("id", "evento", "to_phone", "template_name", "status", "tentativas", "proxima_tentativa_em", "criado_em")
    list_filter = ("status", "evento", "template_name")
    search_fields = ("to_phone", "template_name", "meta_message_id")
    readonly_fields = ("criado_em", "enviado_em", "meta_message_id", "tentativas")
