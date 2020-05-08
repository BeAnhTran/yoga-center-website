from django.urls import include, path

from apps.home import views


app_name = 'home'

urlpatterns = [
    path('', views.HomeIndexView.as_view(), name='index'),
]
