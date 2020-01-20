from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='account_login')
def index(request):
    return render(request, 'dashboard/index.html')
