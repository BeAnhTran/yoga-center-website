from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from api.views import (rooms, lessons, card_types)

app_name = 'api'


urlpatterns = [
    url(r'^rooms/$', rooms.get_rooms_list.as_view(), name='rooms-list'),
    url(r'^lessons/in-range-time/$', lessons.get_lesson_list_in_range_time.as_view(),
        name='lessons-list-in-range-time'),
    path('card-types/for-course/',
         card_types.get_card_types_for_course.as_view(), name='card-type-list-for-course'),
]
