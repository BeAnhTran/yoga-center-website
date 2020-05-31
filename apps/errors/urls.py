from django.urls import include, path
from apps.errors import views


app_name = 'errors'

urlpatterns = [
    path('403/', views._403, name='error-403'),
    path('404/', views._404, name='error-404'),
    path('500/', views._500, name='error-500'),
]
