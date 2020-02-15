from django.urls import include, path
from django.conf.urls import url

from rooms.views import (get_rooms_list)

app_name = 'rooms'

urlpatterns = [
    url(r'^list/json/$', get_rooms_list.as_view(), name='json-list'),
]
