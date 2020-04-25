from django.urls import include, path
from django.conf.urls import url

from apps.feedback import views

app_name = 'feedback'

urlpatterns = [
    path('create/', views.create_feedback, name='create'),
]
