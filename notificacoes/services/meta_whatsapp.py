import json
import os
import urllib.request
import urllib.error

GRAPH_BASE = "https://graph.facebook.com"

def _get_env(name: str, default: str = "") -> str:
    v = os.getenv(name, default)
    return v.strip() if isinstance(v, str) else v

def send_template_message(*, phone_number_id: str, access_token: str, to_phone: str, template_name: str,
                          language_code: str = "pt_BR", components: list | None = None,
                          api_version: str = "v22.0") -> tuple[bool, dict, str]:
    """Envia template message via WhatsApp Cloud API.

    Retorna: (ok, response_json, error_text)
    """
    if components is None:
        components = []

    url = f"{GRAPH_BASE}/{api_version}/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code},
        },
    }
    if components:
        payload["template"]["components"] = components

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {access_token}")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return True, json.loads(body or "{}"), ""
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8")
        except Exception:
            body = str(e)
        return False, {}, body
    except Exception as e:
        return False, {}, str(e)

def resolve_credentials(outbox_obj) -> tuple[str, str, str]:
    """Retorna (api_version, phone_number_id, access_token).
    Prioridade: canal (se preenchido) -> ENV.
    """
    api_version = _get_env("WHATSAPP_API_VERSION", "v22.0")

    phone_number_id = ""
    access_token = ""

    canal = getattr(outbox_obj, "canal", None)
    if canal:
        phone_number_id = (getattr(canal, "phone_number_id", "") or "").strip()
        access_token = (getattr(canal, "access_token", "") or "").strip()

    if not phone_number_id:
        phone_number_id = _get_env("WHATSAPP_PHONE_NUMBER_ID")
    if not access_token:
        access_token = _get_env("WHATSAPP_ACCESS_TOKEN")

    return api_version, phone_number_id, access_token
