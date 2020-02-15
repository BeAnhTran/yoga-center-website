from django.urls import include, path
from django.conf.urls import url

from lessons.views import (get_lesson_list_in_range_time)

app_name = 'lessons'

urlpatterns = [
    url(r'^list/json/$', get_lesson_list_in_range_time.as_view(), name='json-list-in-range-time'),
]
