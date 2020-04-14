from django.urls import include, path
from django.conf.urls import url

from .views import (CourseListView, CourseDetailView)

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$',
        CourseDetailView.as_view(), name='detail'),
]
