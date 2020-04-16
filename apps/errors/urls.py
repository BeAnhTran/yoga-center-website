from django.urls import include, path
from apps.errors import views


app_name = 'errors'

urlpatterns = [
    path('401/', views._401, name='error-401'),
]
