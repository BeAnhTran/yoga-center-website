from django.shortcuts import redirect, render, reverse
from django.views.generic import TemplateView
from apps.accounts.forms.trainee_form import TraineeSignupForm
from allauth.account.views import SignupView
from django.views.generic import CreateView
from django.views import View
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy


class SignUpView(View):
    template_name = 'registration/signup.html'

    def get(self, request):
        if request.GET.get('next') is not None:
            return redirect(reverse('accounts:trainee-signup') + '?next=' + self.request.GET.get('next'))
        #context = {}
        #return render(request, self.template_name, context=context)
        return redirect('accounts:trainee-signup')


class TraineeSignUpView(SignupView):
    # model = User
    # custom template
    template_name = 'registration/trainee_signup_form.html'
    # the previously created form class
    form_class = TraineeSignupForm

    def get_context_data(self, **kwargs):
        ret = super(TraineeSignUpView, self).get_context_data(**kwargs)
        if self.request.session.get('sign_up_from_home') is not None:
            ret['form'].fields['email'].initial = self.request.session.get('sign_up_from_home')[
                'email']
            ret['form'].fields['first_name'].initial = self.request.session.get(
                'sign_up_from_home')['first_name']
            ret['form'].fields['last_name'].initial = self.request.session.get(
                'sign_up_from_home')['last_name']
            ret['form'].fields['phone_number'].initial = self.request.session.get(
                'sign_up_from_home')['phone_number']
            ret['form'].fields['health_condition'].initial = self.request.session.get(
                'sign_up_from_home')['health_condition']
        return ret

    def form_valid(self, form):
        self.user = form.save(self.request)
        if self.request.session.get('sign_up_from_home') is not None:
            del self.request.session['sign_up_from_home']
        messages.success(
            self.request,
            _('Signup successfully'))
        if self.request.GET.get('next') is not None:
            return redirect(reverse('account_login') + '?next=' + self.request.GET.get('next'))
        return redirect(reverse('account_login'))


class TrainerSignUpView(CreateView):
    pass
