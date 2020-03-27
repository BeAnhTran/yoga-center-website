from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from allauth.account.views import SignupView
# from ..models import User
from core.forms.trainee_forms import TraineeSignupForm


class TraineeSignUpView(SignupView):
    # model = User
    # custom template
    template_name = 'registration/trainee_signup_form.html'
    # the previously created form class
    form_class = TraineeSignupForm

    def form_valid(self, form):
        self.user = form.save(self.request)
        return redirect('account_login')
