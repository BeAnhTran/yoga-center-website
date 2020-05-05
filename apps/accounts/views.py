from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from apps.accounts.forms.trainee_form import TraineeSignupForm
from allauth.account.views import SignupView
from django.views.generic import CreateView
from django.views import View
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class SignUpView(View):
    template_name = 'registration/signup.html'

    def get(self, request):
        #context = {}
        #return render(request, self.template_name, context=context)
        return redirect('accounts:trainee-signup')


class TraineeSignUpView(SignupView):
    # model = User
    # custom template
    template_name = 'registration/trainee_signup_form.html'
    # the previously created form class
    form_class = TraineeSignupForm

    def form_valid(self, form):
        self.user = form.save(self.request)
        messages.success(
            self.request,
            _('Signup successfully'))
        return redirect('account_login')


class TrainerSignUpView(CreateView):
    pass
