from django.urls import include, path
from django.conf.urls import url

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$',
        views.PostDetailView.as_view(), name='detail'),
]
