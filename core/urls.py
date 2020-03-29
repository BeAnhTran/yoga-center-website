from django.urls import include, path

from .views import core, trainees, trainers, errors
from core.views.profile import index, trainee
from roll_calls.views import GetRollCallListApiView

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

    # get Roll Call List for CARD, render to FullCalendar
    path('accounts/cards/<int:pk>/roll-call-list', GetRollCallListApiView.as_view(),
         name='profile-trainee-cards-roll-call-list'),

    # EXTEND CARD REQUEST
    path('accounts/cards/<int:pk>/extend/', trainee.TraineeCardExtendView.as_view(),
         name='profile-trainee-card-extend'),
    path('accounts/cards/<int:card_id>/extend-card-request/<int:pk>/', trainee.ExtendCardRequestDetailView.as_view(),
         name='profile-trainee-card-extend-request-detail'),
    path('accounts/cards/<int:card_id>/extend-card-request/<int:pk>/edit', trainee.ExtendCardRequestEditView.as_view(),
         name='profile-trainee-card-extend-request-edit'),
    path('accounts/cards/<int:card_id>/extend-card-request/<int:pk>/delete', trainee.detele_extend_card_request,
         name='profile-trainee-card-extend-request-delete'),

    # REFUND REQUEST
    path('accounts/cards/<int:pk>/refunds/new/', trainee.RefundNewView.as_view(),
         name='profile-trainee-card-refunds-new'),
    path('accounts/cards/<int:card_id>/refunds/<int:pk>/', trainee.RefundDetailView.as_view(),
         name='profile-trainee-card-refunds-detail'),
    path('accounts/cards/<int:card_id>/refunds/<int:pk>/edit', trainee.RefundEditView.as_view(),
         name='profile-trainee-card-refunds-edit'),
    path('accounts/cards/<int:card_id>/refunds/<int:pk>/delete', trainee.detele_refund_request,
         name='profile-trainee-card-refunds-delete'),

    path('401', errors._401, name='error_401'),
]
