"""
Middlewares.
"""
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

def get_current_user():
    """
    Method to get the current user.
    """
    return getattr(_thread_locals, 'user', None)

class ThreadLocalsMiddleware(object):
    """
    Middleware to store the current user and request to thread locals.
    """
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
