import os
import re
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from notificacoes.models import WhatsAppOutbox

def normalize_phone_br(phone: str) -> str:
    if not phone:
        return ""
    digits = re.sub(r"\D+", "", str(phone))
    if digits.startswith("0"):
        digits = digits.lstrip("0")
    if digits.startswith("55"):
        return digits
    if len(digits) >= 10:
        return "55" + digits
    return digits

def get_cliente_phone(cliente) -> str:
    for attr in ["whatsapp", "telefone_whatsapp", "celular", "telefone", "phone"]:
        v = getattr(cliente, attr, None)
        if v:
            return str(v)
    return ""

def tpl(name_env: str, default: str) -> str:
    return (os.getenv(name_env, default) or default).strip()

def enqueue_template(*, to_phone: str, template_name: str, evento: str, components: list | None = None):
    to_phone_n = normalize_phone_br(to_phone)
    if not to_phone_n:
        return
    WhatsAppOutbox.objects.create(
        evento=evento,
        to_phone=to_phone_n,
        template_name=template_name,
        language_code="pt_BR",
        components_json=components or [],
        status="PENDENTE",
        proxima_tentativa_em=timezone.now(),
    )

try:
    from agenda.models import Agendamento
except Exception:
    Agendamento = None

if Agendamento:
    @receiver(post_save, sender=Agendamento)
    def agendamento_post_save(sender, instance, created, **kwargs):
        cliente = getattr(instance, "cliente", None)
        if not cliente:
            return
        phone = get_cliente_phone(cliente)
        if not phone:
            return

        status = getattr(instance, "status", "") or ""
        status_u = str(status).upper()

        if created:
            template_name = tpl("WHATSAPP_TPL_AGENDAMENTO_CRIADO", "agendamento_criado")
            enqueue_template(to_phone=phone, template_name=template_name, evento="AGENDAMENTO_CRIADO")
            return

        if "REALIZ" in status_u:
            template_name = tpl("WHATSAPP_TPL_AGENDAMENTO_REALIZADO", "agendamento_realizado")
            enqueue_template(to_phone=phone, template_name=template_name, evento="AGENDAMENTO_REALIZADO")
        else:
            template_name = tpl("WHATSAPP_TPL_AGENDAMENTO_ATUALIZADO", "agendamento_atualizado")
            enqueue_template(to_phone=phone, template_name=template_name, evento="AGENDAMENTO_ATUALIZADO")
