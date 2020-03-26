from django.urls import include, path

from .views import core, trainees, trainers, errors
from core.views.profile import index, trainee


app_name = 'core'

urlpatterns = [
    path('', core.home, name='home'),
    path('accounts/signup/', core.SignUpView.as_view(), name='account_signup'),
    path('accounts/signup/trainee/',
         trainees.TraineeSignUpView.as_view(), name='trainee_signup'),
    path('accounts/signup/trainer/',
         trainers.TrainerSignUpView.as_view(), name='trainer_signup'),
    path('accounts/profile/', index.ProfileView.as_view(), name='profile'),
    path('accounts/trainee/update-health-condition',
         index.update_health_condition, name='update-health-condition'),
    path('accounts/cards/', trainee.TraineeCardsView.as_view(),
         name='profile-trainee-cards'),
    path('accounts/cards/<int:pk>/', trainee.TraineeCardDetailView.as_view(),
         name='profile-trainee-cards-detail'),
    path('accounts/cards/<int:pk>/extend/', trainee.TraineeCardExtendView.as_view(),
         name='profile-trainee-card-extend'),
    path('401', errors._401, name='error_401'),
]
