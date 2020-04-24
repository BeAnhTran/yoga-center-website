from django.urls import include, path
from django.conf.urls import url

from apps.faq import views

app_name = 'faq'

urlpatterns = [
    path('', views.FAQListView.as_view(), name='list'),
]
