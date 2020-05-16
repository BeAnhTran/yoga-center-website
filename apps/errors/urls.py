from django.urls import include, path
from apps.errors import views


app_name = 'errors'

urlpatterns = [
    path('403/', views._403, name='error-403'),
]
