from django.shortcuts import redirect, render
from django.http import HttpResponse


def _403(request):
    return render(request, '403.html')
