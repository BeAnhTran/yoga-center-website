from django.urls import include, path
from django.conf.urls import url

from apps.classes import views

app_name = 'classes'

urlpatterns = [
    path('', views.YogaClassListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$',
        views.YogaClassDetailView.as_view(), name='detail'),
    path('<slug:slug>/enroll/', views.YogaClassEnrollView.as_view(), name='enroll'),
    path('<slug:slug>/enroll/payment/',
         views.YogaClassEnrollPaymentView.as_view(), name='enroll-payment'),
    path('<slug:slug>/enroll/momo-payment/',
         views.YogaClassEnrollMOMOPaymentView.as_view(), name='enroll-momo-payment'),
    path('<slug:slug>/payment-result/',
         views.YogaClassPaymentResultView.as_view(), name='payment-result'),
    path('<slug:slug>/lessons/', views.YogaClassGetLessonListView.as_view(),
         name='get-list-lesson'),
    path('<slug:slug>/enroll/payment/use-code/', views.UsePromotionCodeView.as_view(),
         name='use-promotion-code-when-payment'),
]
