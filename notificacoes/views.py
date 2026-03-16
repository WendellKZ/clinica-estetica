import json
import os
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "")

def webhook(request):
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge or "", status=200)
        return HttpResponse("forbidden", status=403)
    return HttpResponse("method not allowed", status=405)

@csrf_exempt
def webhook_events(request):
    if request.method != "POST":
        return HttpResponse("method not allowed", status=405)

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except Exception:
        payload = {}

    # TODO (premium+): atualizar status do Outbox com base em message_status
    return JsonResponse({"ok": True})
