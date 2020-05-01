from django.urls import include, path

from apps.accounts import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='sign-up'),
    path('signup/trainee/',
         views.TraineeSignUpView.as_view(), name='trainee-signup'),
    path('signup/trainer/',
         views.TrainerSignUpView.as_view(), name='trainer-signup'),
]
