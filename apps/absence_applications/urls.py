from django.urls import include, path
from apps.absence_applications import views

app_name = 'absence_applications'

urlpatterns = [
    path('new/', views.AbsenceApplicationApiNewView.as_view(),
         name='absence-applications-new'),
]
