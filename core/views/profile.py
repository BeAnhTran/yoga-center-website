from django.shortcuts import redirect, render
from django.views.generic import TemplateView


def index(request):
    return render(request, 'profile/index.html')
