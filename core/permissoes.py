from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def require_perm(perm_codename: str):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.has_perm(perm_codename):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped
    return decorator
