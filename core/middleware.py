from django.conf import settings
from django.http import HttpResponseNotFound

class AdminBlockerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin"):
            allowed_users = set(getattr(settings, "ADMIN_DEV_USERNAMES", []) or [])
            allowed_emails = set(getattr(settings, "ADMIN_DEV_EMAILS", []) or [])

            user = getattr(request, "user", None)
            ok = False

            if user and user.is_authenticated:
                if allowed_users and user.username in allowed_users:
                    ok = True
                if allowed_emails and (user.email or "").lower() in {e.lower() for e in allowed_emails}:
                    ok = True

            if not ok:
                return HttpResponseNotFound("Not Found")

        return self.get_response(request)
