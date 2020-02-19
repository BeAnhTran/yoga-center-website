from django.urls import include, path
from django.conf.urls import url

from .views import (YogaClassListView, YogaClassDetailView,
                    YogaClassEnrollView, YogaClassGetLessonListView, YogaClassEnrollPaymentView)

app_name = 'classes'

urlpatterns = [
    path('', YogaClassListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$',
        YogaClassDetailView.as_view(), name='detail'),
    path('<slug:slug>/enroll/', YogaClassEnrollView.as_view(), name='enroll'),
    path('<slug:slug>/enroll/payment/', YogaClassEnrollPaymentView.as_view(), name='enroll-payment'),
    path('<slug:slug>/lessons/', YogaClassGetLessonListView.as_view(),
         name='get-list-lesson'),
]
