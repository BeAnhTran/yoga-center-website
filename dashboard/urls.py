from django.urls import include, path
from django.conf.urls import url

from .views import dashboard_view, courses_view, rooms_view, lessons_view

app_name = 'dashboard'

urlpatterns = [
    # DASHBOARD
    path('', dashboard_view.index, name='index'),
    # COURSE
    path('courses/', courses_view.CourseListView.as_view(), name='courses-list'),
    path('courses/new/', courses_view.CourseNewView.as_view(), name='courses-new'),
    url(r'^courses/edit/(?P<slug>[\w-]+)/$',
        courses_view.CourseEditView.as_view(), name='courses-update'),
    path('courses/<int:pk>/delete/',
         courses_view.CourseDeleteView.as_view(), name='courses-delete'),
    # ROOMS
    path('rooms/', rooms_view.RoomListView.as_view(), name='rooms-list'),
    path('rooms/<int:pk>/', rooms_view.RoomDetailView.as_view(), name='rooms-detail'),
    path('rooms/<int:pk>/lessons/',
         rooms_view.get_lessons, name='rooms-get-lessons'),
    # LESSONS
    path('lessons/detail/json/', lessons_view.detail_json, name='lessons-detail-json'),
]
