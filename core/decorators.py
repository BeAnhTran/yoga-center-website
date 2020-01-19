from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def trainee_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    '''
    Decorator for views that checks that the logged in user is a trainee,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_trainee,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def trainer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    '''
    Decorator for views that checks that the logged in user is a trainer,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_trainer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
