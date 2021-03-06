from functools import wraps
from django.shortcuts import render, redirect


def staff_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        if request.user.is_active and request.user.is_staff or request.user.is_superuser:
            pass
        else:
            return redirect('errors:error-403')

        return function(request, *args, **kwargs)

    return wrap


def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        if request.user.is_active and request.user.is_superuser:
            pass
        else:
            return redirect('errors:error-403')

        return function(request, *args, **kwargs)

    return wrap
