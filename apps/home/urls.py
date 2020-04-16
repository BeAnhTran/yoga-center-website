from django.urls import include, path

from apps.home import views


app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
]
