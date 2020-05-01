from django.urls import include, path
from django.conf.urls import url

from apps.donations import views

app_name = 'donations'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
