from django.urls import include, path

from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', index, name='index'),
    path('courses/', CourseListView.as_view(), name='list_course'),
    path('courses/new/', CourseNewView.as_view(), name='new_course'),
]
