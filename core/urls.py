from django.urls import include, path

from .views import core, trainees, trainers, errors, profile

app_name = 'core'

urlpatterns = [
    path('', core.home, name='home'),
    path('accounts/signup/', core.SignUpView.as_view(), name='account_signup'),
    path('accounts/signup/trainee/',
         trainees.TraineeSignUpView.as_view(), name='trainee_signup'),
    path('accounts/signup/trainer/',
         trainers.TrainerSignUpView.as_view(), name='trainer_signup'),
    path('accounts/profile/', profile.ProfileView.as_view(), name='profile'),
    path('accounts/trainee/update-health-condition',
         profile.update_health_condition, name='update-health-condition'),
    path('401', errors._401, name='error_401'),
]
