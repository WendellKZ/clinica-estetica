import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from notificacoes.models import WhatsAppOutbox
from notificacoes.services.meta_whatsapp import send_template_message, resolve_credentials

class Command(BaseCommand):
    help = "Envia fila de WhatsApp (Outbox) via Meta Cloud API. Use --once para executar uma vez."

    def add_arguments(self, parser):
        parser.add_argument("--once", action="store_true", help="Executa só 1 ciclo e sai.")
        parser.add_argument("--sleep", type=int, default=15, help="Segundos entre ciclos (modo contínuo).")
        parser.add_argument("--limit", type=int, default=10, help="Qtde máxima por ciclo.")
        parser.add_argument("--max-attempts", type=int, default=8, help="Tentativas máximas antes de parar.")
        parser.add_argument("--retry-minutes", type=int, default=10, help="Minutos para próxima tentativa após erro.")

    def handle(self, *args, **opts):
        once = opts["once"]
        sleep_s = opts["sleep"]
        limit = opts["limit"]
        max_attempts = opts["max_attempts"]
        retry_minutes = opts["retry_minutes"]

        while True:
            sent = self._process(limit=limit, max_attempts=max_attempts, retry_minutes=retry_minutes)
            if once:
                break
            time.sleep(sleep_s if sent == 0 else 1)

    def _process(self, *, limit: int, max_attempts: int, retry_minutes: int) -> int:
        now = timezone.now()
        qs = (WhatsAppOutbox.objects
              .select_related("canal")
              .filter(status__in=["PENDENTE", "ERRO"], proxima_tentativa_em__lte=now)
              .order_by("proxima_tentativa_em", "id")[:limit])

        count = 0
        for item in qs:
            with transaction.atomic():
                item.status = "ENVIANDO"
                item.save(update_fields=["status"])

            api_version, phone_number_id, access_token = resolve_credentials(item)
            if not phone_number_id or not access_token:
                self._mark_error(item, "Credenciais WhatsApp ausentes (PHONE_NUMBER_ID / ACCESS_TOKEN).", retry_minutes, max_attempts)
                continue

            ok, resp, err = send_template_message(
                phone_number_id=phone_number_id,
                access_token=access_token,
                to_phone=item.to_phone,
                template_name=item.template_name,
                language_code=item.language_code,
                components=item.components_json or [],
                api_version=api_version,
            )

            if ok:
                msg_id = ""
                try:
                    msg_id = (resp.get("messages") or [{}])[0].get("id", "") or ""
                except Exception:
                    msg_id = ""
                item.status = "ENVIADO"
                item.enviado_em = timezone.now()
                item.meta_message_id = msg_id
                item.ultimo_erro = ""
                item.save(update_fields=["status", "enviado_em", "meta_message_id", "ultimo_erro"])
                count += 1
            else:
                self._mark_error(item, err, retry_minutes, max_attempts)
        return count

    def _mark_error(self, item, err: str, retry_minutes: int, max_attempts: int):
        item.tentativas = (item.tentativas or 0) + 1
        item.ultimo_erro = (err or "")[:4000]
        if item.tentativas >= max_attempts:
            item.status = "ERRO"
            item.proxima_tentativa_em = timezone.now() + timezone.timedelta(days=3650)
        else:
            item.status = "ERRO"
            item.proxima_tentativa_em = timezone.now() + timezone.timedelta(minutes=retry_minutes)
        item.save(update_fields=["status", "tentativas", "ultimo_erro", "proxima_tentativa_em"])
