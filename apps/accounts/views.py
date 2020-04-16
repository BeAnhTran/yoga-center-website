from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from apps.accounts.forms.trainee_form import TraineeSignupForm
from allauth.account.views import SignupView
from django.views.generic import CreateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class TraineeSignUpView(SignupView):
    # model = User
    # custom template
    template_name = 'registration/trainee_signup_form.html'
    # the previously created form class
    form_class = TraineeSignupForm

    def form_valid(self, form):
        self.user = form.save(self.request)
        return redirect('account_login')


class TrainerSignUpView(CreateView):
    pass
