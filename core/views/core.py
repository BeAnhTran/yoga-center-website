from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    context = {
        'active_nav': 'home'
    }
    return render(request, 'core/home.html', context=context)
