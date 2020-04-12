from django.urls import include, path
from django.conf.urls import url
from promotions import views

app_name = 'promotions'

urlpatterns = [
    path('codes/check/', views.CheckCodeApiView.as_view(), name='codes-check'),
]
