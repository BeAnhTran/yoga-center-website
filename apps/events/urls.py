from django.urls import include, path
from django.conf.urls import url

from apps.events import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$',
        views.EventDetailView.as_view(), name='detail'),
]
