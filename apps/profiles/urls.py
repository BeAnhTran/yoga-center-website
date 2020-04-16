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

    # EXTEND CARD REQUEST
    path('accounts/cards/<int:pk>/extend/', profile_trainee_view.TraineeCardExtendView.as_view(),
         name='profile-trainee-card-extend'),
    path('accounts/cards/<int:card_id>/extend-card-request/<int:pk>/', profile_trainee_view.ExtendCardRequestDetailView.as_view(),
         name='profile-trainee-card-extend-request-detail'),
    path('accounts/cards/<int:card_id>/extend-card-request/<int:pk>/edit', profile_trainee_view.ExtendCardRequestEditView.as_view(),
         name='profile-trainee-card-extend-request-edit'),
    path('accounts/cards/<int:card_id>/extend-card-request/<int:pk>/delete', profile_trainee_view.detele_extend_card_request,
         name='profile-trainee-card-extend-request-delete'),

    # REFUND REQUEST
    path('accounts/cards/<int:pk>/refunds/new/', profile_trainee_view.RefundNewView.as_view(),
         name='profile-trainee-card-refunds-new'),
    path('accounts/cards/<int:card_id>/refunds/<int:pk>/', profile_trainee_view.RefundDetailView.as_view(),
         name='profile-trainee-card-refunds-detail'),
    path('accounts/cards/<int:card_id>/refunds/<int:pk>/edit', profile_trainee_view.RefundEditView.as_view(),
         name='profile-trainee-card-refunds-edit'),
    path('accounts/cards/<int:card_id>/refunds/<int:pk>/delete', profile_trainee_view.detele_refund_request,
         name='profile-trainee-card-refunds-delete'),
]
