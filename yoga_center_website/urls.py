"""yoga_center_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.urls import path
import notifications.urls


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    # home page
    path('', include('apps.home.urls')),
    #
    path('accounts/', include('apps.accounts.urls')),
    # profile
    path('accounts/profile/', include('apps.profiles.urls')),
    # errors
    path('errors/', include('apps.errors.urls')),
    # courses
    path('courses/', include('apps.courses.urls')),
    # classes
    path('classes/', include('apps.classes.urls')),
    # rooms
    path('rooms/', include('apps.rooms.urls')),
    # lessons
    path('lessons/', include('apps.lessons.urls')),
    # make-up lessons
    path('make-up-lessons/', include('apps.make_up_lessons.urls')),
    # card types
    path('card-types/', include('apps.card_types.urls')),
    # schedule
    path('schedule/', include('apps.yoga_schedule.urls')),
    # trainers
    path('trainers/', include('apps.trainers.urls')),
    # blog
    path('blog/', include('apps.blog.urls')),
    # shop
    path('shop/', include('apps.shop.urls')),
    # promotions
    path('promotions/', include('apps.promotions.urls')),
    # events
    path('events/', include('apps.events.urls')),
    # FAQ
    path('faq/', include('apps.faq.urls')),
    # feedback
    path('feedback/', include('apps.feedback.urls')),
    # donations
    path('donations/', include('apps.donations.urls')),
    # dashboard
    path('dashboard/', include('apps.dashboard.urls')),
    # absence applications
    path('absence-applications/', include('apps.absence_applications.urls')),
    # admin site
    path('admin/', admin.site.urls),
    # accounts
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url('notifications/', include(notifications.urls)),
) + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
