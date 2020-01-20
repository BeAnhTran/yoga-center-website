from django.urls import include, path
from django.conf.urls import url

from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', index, name='index'),
    path('courses/', CourseListView.as_view(), name='list_course'),
    path('courses/new/', CourseNewView.as_view(), name='new_course'),
    url(r'^courses/edit/(?P<slug>[\w-]+)/$',
        CourseEditView.as_view(), name='update_course'),
    path('courses/<int:pk>/delete/',
         CourseDeleteView.as_view(), name='delete_course'),
]
