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

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    # index page
    path('', include('core.urls')),
    # courses
    path('courses/', include('courses.urls')),
    # classes
    path('classes/', include('classes.urls')),
    # schedule
    path('schedule/', include('yoga_schedule.urls')),
    # dashboard
    path('dashboard/', include('dashboard.urls')),
    # admin site
    path('admin/', admin.site.urls),
    # accounts
    url(r'^accounts/', include('allauth.urls')),
) + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# API 
# support get data when using ajax
urlpatterns += [
    path('api/', include('api.urls')),
]
