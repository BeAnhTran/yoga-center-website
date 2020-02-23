from django.urls import include, path
from django.conf.urls import url

from .views import (
    dashboard_view, courses_view, rooms_view,
    lessons_view, classes_view, cards_view,
    card_types_view, trainees_view, trainers_view, staffs_view,
    admins_view, roll_calls_view)

app_name = 'dashboard'

# COURSE
courses_urlpatterns = [
    path('', courses_view.CourseListView.as_view(), name='courses-list'),
    path('new/', courses_view.CourseNewView.as_view(), name='courses-new'),
    url(r'^edit/(?P<slug>[\w-]+)/$',
        courses_view.CourseEditView.as_view(), name='courses-update'),
    path('<int:pk>/delete/',
         courses_view.CourseDeleteView.as_view(), name='courses-delete'),
]

# CLASSES
classes_urlpatterns = [
    path('', classes_view.ClassListView.as_view(), name='classes-list'),
    path('new/', classes_view.ClassNewView.as_view(), name='classes-new'),
    path('<int:pk>/', classes_view.ClassDetailView.as_view(),
         name='classes-detail'),
    path('<int:pk>/schedule/',
         classes_view.ClassScheduleView.as_view(), name='classes-schedule'),
    url(r'^edit/(?P<slug>[\w-]+)/$',
        classes_view.ClassEditView.as_view(), name='classes-update'),
    path('<int:pk>/delete/',
         classes_view.ClassDeleteView.as_view(), name='classes-delete'),
    path('<int:pk>/lessons/',
         classes_view.get_lessons, name='classes-get-lessons'),
    # create lessen for a class
    path('<int:pk>/lessons/new/',
         classes_view.create_lessons, name='classes-create-new-lesson'),
]

# LESSONS
lessons_urlpatterns = [
    path('', lessons_view.LessonListView.as_view(), name='lessons-list'),
    url(r'^(?P<pk>[0-9]+)$', lessons_view.LessonDetailApiView.as_view(),
        name='lessons-detail-json'),
    url(r'^(?P<pk>[0-9]+)/roll-calls/$', lessons_view.ListRollCallApiView.as_view(),
        name='lessons-roll-calls'),
]

# ROOMS
rooms_urlpatterns = [
    path('', rooms_view.RoomListView.as_view(), name='rooms-list'),
    path('<int:pk>/', rooms_view.RoomDetailView.as_view(), name='rooms-detail'),
    path('<int:pk>/lessons/',
         rooms_view.get_lessons, name='rooms-get-lessons'),
]

# CARDS
cards_urlpatterns = [
    path('', cards_view.CardListView.as_view(), name='cards-list'),
]

# CARD TYPES
card_types_urlpatterns = [
    path('', card_types_view.CardTypeListView.as_view(),
         name='card-types-list'),
    path('for-course/', card_types_view.get_card_types_for_course.as_view(),
         name='json-card-type-list-for-course'),
]

# TRAINEES
trainees_urlpatterns = [
    path('', trainees_view.TraineeListView.as_view(), name='trainees-list')
]

# TRAINERS
trainers_urlpatterns = [
    path('', trainers_view.TrainerListView.as_view(), name='trainers-list')
]

# STAFFS
staffs_urlpatterns = [
    path('', staffs_view.StaffListView.as_view(), name='staffs-list')
]

# STAFFS
admins_urlpatterns = [
    path('', admins_view.AdminListView.as_view(), name='admins-list')
]

# ROLL CALLS
roll_calls_urlpatterns = [
    path('<int:pk>/', roll_calls_view.RollCallDetail.as_view(), name='roll-calls-detail'),
]

# DASHBOARD
urlpatterns = [
    path('', dashboard_view.index, name='index'),
    path('courses/', include(courses_urlpatterns)),
    path('classes/', include(classes_urlpatterns)),
    path('lessons/', include(lessons_urlpatterns)),
    path('rooms/', include(rooms_urlpatterns)),
    path('cards/', include(cards_urlpatterns)),
    path('card-types/', include(card_types_urlpatterns)),
    path('trainees/', include(trainees_urlpatterns)),
    path('trainers/', include(trainers_urlpatterns)),
    path('staffs/', include(staffs_urlpatterns)),
    path('admins/', include(admins_urlpatterns)),
    path('roll-calls/', include(roll_calls_urlpatterns)),
]
