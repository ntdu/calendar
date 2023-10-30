# -*- coding: utf-8 -*-
import logging

from core import constants
from datetime import datetime, timedelta
from django_redis import get_redis_connection
from fcm_django.models import FCMDevice
from firebase_admin import messaging
from celery import shared_task
from src.dj_project import celery_app
from django.core.exceptions import ObjectDoesNotExist
from src.notification.models import Notification, User
from src.notification.serializers import GetMergedNotificationSerializer

redis_client = get_redis_connection()
logger = logging.getLogger(constants.CONSOLE_LOGGER)


from django_celery_beat.models import IntervalSchedule, PeriodicTask
import requests
import json

@shared_task(name='update_calender', soft_time_limit=3600)
def check_calender():
    users = User.objects.all()
    for user in users:
        headers = {"Authorization": f"Bearer {user.calendar_access_token}"}

        date = datetime.utcnow() + timedelta(hours=7)
        date_str = date.strftime("%Y-%m-%d")

        from_time = f"{date_str}T23:59:59%2B07:00"
        to_time = f"{date_str}T00:00:00%2B07:00"

        url = f'https://www.googleapis.com/calendar/v3/calendars/{user.email}/events?timeMax={from_time}&timeMin={to_time}&singleEvents=true'
        x = requests.get(url, headers=headers)

        if x.status_code != 200:
            form_data = {
                'client_id': user.client_id,
                'client_secret': user.client_secret,
                'refresh_token': user.calendar_refresh_token,
                'grant_type': 'refresh_token',
            }

            url = f'https://oauth2.googleapis.com/token'
            refresh_rps = requests.post(url, data=form_data)

            new_access_token = refresh_rps.json().get('access_token')
            user.calendar_access_token = new_access_token
            user.save()

            headers = {"Authorization": f"Bearer {new_access_token}"}
            url = f'https://www.googleapis.com/calendar/v3/calendars/{user.email}/events?timeMax={from_time}&timeMin={to_time}&singleEvents=true'
            x = requests.get(url, headers=headers)


        calendar_lst = x.json()

        for item in calendar_lst.get('items'):
            if not item.get('summary'):
                continue

            if Notification.objects.filter(calendar_id=item.get('id'), created_at__date=datetime.utcnow()).first():
                continue

            print(item.get('summary', ''))
            print(item.get('start', {}).get('dateTime'))
            print("=" * 100)

            noti = Notification.objects.create(
                calendar_id=item.get('id'),
                user=user,
                creator=item.get('creator', {}).get('email'),
                summary=item.get('summary', ''),
                location=item.get('location', ''),
                htmlLink=item.get('htmlLink', ''),
                start=item.get('start', {}).get('dateTime'),
                end=item.get('end', {}).get('dateTime')
            )

            noti = Notification.objects.filter(calendar_id=item.get('id'), created_at__date=date).first()
            specific_time = noti.start - timedelta(minutes=10)

            if noti.created_at + timedelta(minutes=10) > noti.start:
                send_calendar_task.apply_async((noti.id,), countdown=1)
            else:
                send_calendar_task.apply_async((noti.id,), eta=specific_time)


from src.notification.serializers import (
    GetNotificationSerializer
)


APP_AUTHEN_WORKCHAT = 'Basic YWRtaW46YWRtaW4='
URL_NOTIFICATION_WORKCHAT = 'http://172.27.230.25:4000/notification_mgmt/api/notify_user_text_msg/'


def send_notification_to_workchat(email, text):
    print("Call send_notification_to_workchat")
    header = {
        'Authorization': APP_AUTHEN_WORKCHAT,
        'Content-Type': 'application/json'
    }
    body = {
        "to_email": f"{email}",
        "type": "facebook_workplace",
        "content": f"{text}"
    }
    try:
        response = requests.post(
            url=URL_NOTIFICATION_WORKCHAT,
            json=body,
            headers=header
        )

        print(response)
        print("=" * 100)
    except Exception as e:
        print(e)


@shared_task(name='send_calendar', soft_time_limit=3600)
def send_calendar_task(noti_id):
    print("send_calendar_task")
    print(noti_id)
    try:
        noti = Notification.objects.get(pk=noti_id)
    except ObjectDoesNotExist:
        logger.info(f'not found reminder {noti_id=}')
        return

    sz = GetNotificationSerializer(noti)

    sz_data = sz.data

    if noti.user.is_workplace_noti:
        send_notification_to_workchat(noti.user.email, f"""
            CALENDAR\nSummary: {sz_data.get('summary')} \nCreator: {sz_data.get('creator')} \nLocation: {sz_data.get('location')} \nHtmlLink: {sz_data.get('htmlLink')} \nStart: {(noti.start + timedelta(hours=7)).strftime("%m/%d/%Y, %H:%M:%S")} \nEnd: {(noti.end + timedelta(hours=7)).strftime("%m/%d/%Y, %H:%M:%S")}\n
        """)

    if noti.user.is_web_noti:
        device = FCMDevice.objects.filter(name=noti.user.email).first()

        if device:
            data = {
                'summary': sz_data.get('summary'),
                'creator': sz_data.get('creator'),
                'location': sz_data.get('location'),
                'htmlLink': sz_data.get('htmlLink'),
                'start': sz_data.get('start'),
                'end': sz_data.get('end')
            }

            device.send_message(
                messaging.Message(
                    data=data
                )
            )

        else:
            print(f"Not found FCMDevice for user_header: {noti.user.email}")

    if noti.user.is_discord_noti:
        pass
