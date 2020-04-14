from django.urls import include, path
from django.conf.urls import url

from .views import index

app_name = 'yoga_schedule'

urlpatterns = [
    path('', index, name='index'),
]
