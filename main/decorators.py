from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from functools import wraps

def superuser_required(view_func):
    """Decorator for views that checks that the user is a superuser."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/admin/login/?next=' + request.path)
        if not request.user.is_superuser:
            return redirect('/admin/login/?next=' + request.path)
        return view_func(request, *args, **kwargs)
    return _wrapped_view