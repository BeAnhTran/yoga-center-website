from django.urls import include, path

from apps.profiles.views import bills_view, profile_view, profile_trainee_view, profile_trainer_view
from apps.roll_calls.views import GetRollCallListApiView


app_name = 'profile'

urlpatterns = [
    path('', profile_view.ProfileView.as_view(), name='index'),
    path('bills/', bills_view.BillListView.as_view(), name='accounts-bills'),
    path('trainee/update-health-condition',
         profile_view.update_health_condition, name='update-health-condition'),
    path('cards/', profile_trainee_view.TraineeCardsView.as_view(),
         name='profile-trainee-cards'),
    path('cards/<int:pk>/', profile_trainee_view.TraineeCardDetailView.as_view(),
         name='profile-trainee-cards-detail'),

    # get Roll Call List for CARD, render to FullCalendar
    path('cards/<int:pk>/roll-call-list', GetRollCallListApiView.as_view(),
         name='profile-trainee-cards-roll-call-list'),

    # REFUND REQUEST
    path('accounts/cards/<int:pk>/refunds/new/', profile_trainee_view.RefundNewView.as_view(),
         name='profile-trainee-card-refunds-new'),
    path('accounts/cards/<int:card_id>/refunds/<int:pk>/', profile_trainee_view.RefundDetailView.as_view(),
         name='profile-trainee-card-refunds-detail'),
    path('accounts/cards/<int:card_id>/refunds/<int:pk>/delete', profile_trainee_view.detele_refund_request,
         name='profile-trainee-card-refunds-delete'),
]
