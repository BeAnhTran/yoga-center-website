from django.shortcuts import redirect, render
from django.http import HttpResponse


def _401(request):
    return HttpResponse('401 Unauthorized', status=401)
