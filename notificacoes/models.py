from django.db import models
from django.utils import timezone

try:
    from empresas.models import Empresa
except Exception:
    Empresa = None

class WhatsAppCanal(models.Model):
    """Canal WhatsApp (Meta Cloud API).
    Para SaaS multi-clínica: 1 canal por Empresa (opcional).
    No MVP: pode ficar vazio e usar ENV.
    """
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True) if Empresa else None
    nome = models.CharField(max_length=120, default="Canal Principal")
    phone_number_id = models.CharField(max_length=64, blank=True, default="")
    waba_id = models.CharField(max_length=64, blank=True, default="")
    access_token = models.TextField(blank=True, default="")  # preferir ENV; aqui é opcional

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.empresa:
            return f"{self.nome} - {self.empresa}"
        return self.nome

class WhatsAppOutbox(models.Model):
    STATUS = (
        ("PENDENTE", "Pendente"),
        ("ENVIANDO", "Enviando"),
        ("ENVIADO", "Enviado"),
        ("ERRO", "Erro"),
    )

    canal = models.ForeignKey(WhatsAppCanal, on_delete=models.SET_NULL, null=True, blank=True)
    evento = models.CharField(max_length=64, blank=True, default="")
    to_phone = models.CharField(max_length=32)
    template_name = models.CharField(max_length=120)
    language_code = models.CharField(max_length=16, default="pt_BR")
    components_json = models.JSONField(default=list, blank=True)

    status = models.CharField(max_length=16, choices=STATUS, default="PENDENTE")
    tentativas = models.PositiveIntegerField(default=0)
    proxima_tentativa_em = models.DateTimeField(default=timezone.now)
    ultimo_erro = models.TextField(blank=True, default="")

    meta_message_id = models.CharField(max_length=128, blank=True, default="")
    criado_em = models.DateTimeField(auto_now_add=True)
    enviado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-criado_em"]
        permissions = [
            ("manage_whatsapp_outbox", "Pode gerenciar fila de WhatsApp"),
        ]

    def __str__(self):
        return f"{self.template_name} -> {self.to_phone} [{self.status}]"
