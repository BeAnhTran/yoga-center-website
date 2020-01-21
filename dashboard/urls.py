from django.urls import include, path
from django.conf.urls import url

from .views import index, course

app_name = 'dashboard'

urlpatterns = [
    path('', index.index, name='index'),
    path('courses/', course.CourseListView.as_view(), name='list_course'),
    path('courses/new/', course.CourseNewView.as_view(), name='new_course'),
    url(r'^courses/edit/(?P<slug>[\w-]+)/$',
        course.CourseEditView.as_view(), name='update_course'),
    path('courses/<int:pk>/delete/',
         course.CourseDeleteView.as_view(), name='delete_course'),
]
