from django.urls import include, path
from django.conf.urls import url
from apps.make_up_lessons import views

app_name = 'make_up_lessons'

urlpatterns = [
    path('<int:pk>/detroy/',
         views.DestroyMakeUpLessonApi.as_view(), name='destroy-register'),
    path('lesson/<int:lesson_pk>/register/',
         views.RegisterMakeUpLessonApi.as_view(), name='register'),

]
