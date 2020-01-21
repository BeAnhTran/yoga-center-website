from django.urls import include, path

from .views import core, trainees, trainers, errors

app_name = 'core'

urlpatterns = [
    path('', core.home, name='home'),
    path('accounts/signup/', core.SignUpView.as_view(), name='account_signup'),
    path('accounts/signup/trainee/',
         trainees.TraineeSignUpView.as_view(), name='trainee_signup'),
    path('accounts/signup/trainer/',
         trainers.TrainerSignUpView.as_view(), name='trainer_signup'),
    path('401', errors._401, name='error_401'),
]
