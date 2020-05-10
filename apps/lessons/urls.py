from django.urls import include, path
from django.conf.urls import url

from apps.lessons import views

app_name = 'lessons'

urlpatterns = [
    url(r'^list/json/$', views.GetLessonListInRangeTimeAPIView.as_view(),
        name='json-list-in-range-time'),
    path('detail/<pk>/', views.LessonDetailAPIView.as_view(), name='json-lesson-api'),
]
