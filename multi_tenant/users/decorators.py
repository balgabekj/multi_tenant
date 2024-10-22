from django.core.exceptions import PermissionDenied
from functools import wraps

def tenant_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'tenant':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def renter_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'renter':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
