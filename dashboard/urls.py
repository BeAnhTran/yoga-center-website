from django.urls import include, path

from .views import index

app_name = 'dashboard'

urlpatterns = [
    path('', index, name='index'),
]
