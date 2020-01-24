from django.urls import include, path
from django.conf.urls import url

from .views import index, course, room

app_name = 'dashboard'

urlpatterns = [
    path('', index.index, name='index'),
    # COURSE
    path('courses/', course.CourseListView.as_view(), name='list_course'),
    path('courses/new/', course.CourseNewView.as_view(), name='new_course'),
    url(r'^courses/edit/(?P<slug>[\w-]+)/$',
        course.CourseEditView.as_view(), name='update_course'),
    path('courses/<int:pk>/delete/',
         course.CourseDeleteView.as_view(), name='delete_course'),
    # ROOMS
    path('rooms/', room.RoomListView.as_view(), name='list_room'),
    path('rooms/<int:pk>/', room.RoomDetailView.as_view(), name='room_detail'),
    path('rooms/<int:pk>/lessons/',
         room.get_lessons, name='room_lessons'),
]
