from django.urls import include, path
from django.conf.urls import url

from .views import (YogaClassListView, YogaClassDetailView)

app_name = 'classes'

urlpatterns = [
    path('', YogaClassListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$',
        YogaClassDetailView.as_view(), name='detail'),
]
