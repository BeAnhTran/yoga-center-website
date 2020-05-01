from django.urls import include, path
from django.conf.urls import url

from apps.trainers import views

app_name = 'trainers'

urlpatterns = [
    path('', views.TrainerListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$',
        views.TrainerDetailView.as_view(), name='detail'),
]
