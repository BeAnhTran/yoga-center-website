from django.urls import include, path

from apps.home import views


app_name = 'home'

urlpatterns = [
    path('', views.HomeIndexView.as_view(), name='index'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
]
