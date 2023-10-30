# -*- coding: utf-8 -*-
"""
URL configuration for noti_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from .service_settings import service_settings
from core.templates import get_health_check_view


urlpatterns = [
    # admin views
    path('admin/', admin.site.urls),

    # health check
    path('server-info/', get_health_check_view(service_settings.SERVICE_NAME, service_settings.SERVICE_PORT)),

    # api views
    path('api/notification/', include("src.notification.urls")),
    re_path(r'^firebase-messaging-sw.js', (TemplateView.as_view(
        template_name="firebase-messaging-sw.js",
        content_type='application/javascript',
    )), name='firebase-messaging-sw.js'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
