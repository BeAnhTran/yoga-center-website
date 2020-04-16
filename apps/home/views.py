from django.shortcuts import redirect, render


def home(request):
    context = {
        'active_nav': 'home'
    }
    return render(request, 'home/index.html', context=context)
