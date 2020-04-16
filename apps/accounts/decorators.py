from functools import wraps
from django.shortcuts import render, redirect


def trainee_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        if request.user.is_active and request.user.is_trainee:
            pass
        else:
            return redirect('errors:error_401')

        return function(request, *args, **kwargs)

    return wrap


def trainer_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        if request.user.is_active and request.user.is_trainer:
            pass
        else:
            return redirect('errors:error_401')

        return function(request, *args, **kwargs)

    return wrap
