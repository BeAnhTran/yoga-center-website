from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from ..decorators import staff_required
from django.contrib.auth.decorators import login_required


@login_required
@staff_required
def index(request):
    context = {
        'active_nav': 'dashboard'
    }
    return render(request, 'dashboard/index.html', context=context)
