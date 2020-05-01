from django.urls import include, path
from django.conf.urls import url

from apps.card_types.views import CardTypeDetailApiView

app_name = 'card_types'

urlpatterns = [
    path('<int:pk>/detail/json/',
         CardTypeDetailApiView.as_view(), name='detail-json'),
]
