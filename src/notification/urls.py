# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from src.notification.views import NotificationView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register(r'', NotificationView)
urlpatterns = router.urls
