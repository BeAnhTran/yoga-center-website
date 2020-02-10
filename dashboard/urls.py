from django.urls import include, path
from django.conf.urls import url

from .views import (dashboard_view, courses_view, rooms_view,
                    lessons_view, classes_view, cards_view, card_types_view)

app_name = 'dashboard'

# DASHBOARD
urlpatterns = [
    path('', dashboard_view.index, name='index'),
]

# COURSE
urlpatterns += [
    path('courses/', courses_view.CourseListView.as_view(), name='courses-list'),
    path('courses/new/', courses_view.CourseNewView.as_view(), name='courses-new'),
    url(r'^courses/edit/(?P<slug>[\w-]+)/$',
        courses_view.CourseEditView.as_view(), name='courses-update'),
    path('courses/<int:pk>/delete/',
         courses_view.CourseDeleteView.as_view(), name='courses-delete'),
]

# CLASSES
urlpatterns += [
    path('classes/', classes_view.ClassListView.as_view(), name='classes-list'),
    path('classes/new/', classes_view.ClassNewView.as_view(), name='classes-new'),
    path('classes/<int:pk>/', classes_view.ClassDetailView.as_view(),
         name='classes-detail'),
    path('classes/<int:pk>/schedule/',
         classes_view.ClassScheduleView.as_view(), name='classes-schedule'),
    url(r'^classes/edit/(?P<slug>[\w-]+)/$',
        classes_view.ClassEditView.as_view(), name='classes-update'),
    path('classes/<int:pk>/delete/',
         classes_view.ClassDeleteView.as_view(), name='classes-delete'),
    path('classes/<int:pk>/lessons/',
         classes_view.get_lessons, name='classes-get-lessons'),
    path('classes/<int:pk>/lessons/new/',
         classes_view.create_lessons, name='classes-create-new-lesson'),
]

# LESSONS
urlpatterns += [
    path('lessons/detail/json/', lessons_view.detail_json,
         name='lessons-detail-json'),
]

# ROOMS
urlpatterns += [
    path('rooms/', rooms_view.RoomListView.as_view(), name='rooms-list'),
    path('rooms/<int:pk>/', rooms_view.RoomDetailView.as_view(), name='rooms-detail'),
    path('rooms/<int:pk>/lessons/',
         rooms_view.get_lessons, name='rooms-get-lessons'),
]

# CARDS
urlpatterns += [
    path('cards/', cards_view.CardListView.as_view(), name='cards-list'),
]

# CARD TYPES
urlpatterns += [
    path('card-types/', card_types_view.CardTypeListView.as_view(),
         name='card-types-list'),
]
