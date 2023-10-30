# -*- coding: utf-8 -*-
from django.db import models
from django_celery_beat.models import PeriodicTask


class User(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    is_web_noti = models.BooleanField(default=True)
    is_workplace_noti = models.BooleanField(default=True)
    is_discord_noti = models.BooleanField(default=True)
    calendar_access_token = models.CharField(max_length=255, null=True, blank=True)
    calendar_refresh_token = models.CharField(max_length=255, null=True, blank=True)
    client_id = models.CharField(max_length=255, null=True, blank=True)
    client_secret = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.email


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)  # user nhận thông báo
    calendar_id = models.CharField(max_length=255)
    creator = models.CharField(max_length=255, default='')
    summary = models.TextField(max_length=255, default='')
    location = models.TextField(default='')
    htmlLink = models.TextField(max_length=255, default='')
    start = models.DateTimeField()
    end = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.email) + " " + self.creator + " " + self.summary