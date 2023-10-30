# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta
import requests
from core import constants
from core.utils import custom_response
from django.shortcuts import render
from firebase_admin import messaging
from fcm_django.models import FCMDevice
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from src.notification.models import Notification, User
from src.notification.serializers import (
    GetNotificationSerializer,
    NotificationSerializer,
    RegisterTokenSerializer,
    RegisterCalendarTokenSerializer,
    UserSerializer
)
from src.utils import pagination_list_data
from src.utils.request_headers import get_email_from_header
from django_celery_beat.models import CrontabSchedule, PeriodicTask

logger = logging.getLogger(constants.CONSOLE_LOGGER)
from src.notification.tasks import check_calender, send_notification_to_workchat


import discord

def handle_user_messages(msg) ->str:
    print("hgeheheh")
    message = msg.lower() #Converts all inputs to lower case
    if message == 'hi':
        return 'Hi there'
    if message =='hello':
        return 'Hello user. Welcome'

async def processMessage(message, user_message):
    try:
        botfeedback = handle_user_messages(user_message)
        await message.channel.send(botfeedback)
    except Exception as error:
        print(error)


def runBot():
    discord_token = 'MTE2MDYxMDA2MDMzMDg4MTA3NA.GdGfkx.lmfbQwzOPk1stjHE8Ng7aqTU_kONahwDJ2ilgM'
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print({client.user}, 'is live')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await processMessage(message, 'hi')

    client.run(discord_token)



class NotificationView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def list(self, request, pk=None):
        try:
            limit_req = request.GET.get('limit', 20)
            offset_req = request.GET.get('offset', 1)

            user_header = get_email_from_header(request.headers)

            noti = Notification.objects.filter(
                user__email=user_header
            ).order_by("-created_at")

            sz = GetNotificationSerializer(noti, many=True)

            data_result = pagination_list_data(sz.data, limit_req, offset_req)
            return custom_response(200, "Lấy danh sách calendar thành công.", data_result)
        except Exception as e:
            logger.info(f"EXCEPTION: get NotificationView ----------{str(e)}")
            return custom_response(500, constants.RESP_MSG_ERROR_IN_SERVER)

    # @action(detail=True, methods=["POST"], url_path="seen-notification")
    # def seen_notification(self, request, pk=None):
    #     try:
    #         user_header = get_user_from_header(request.headers)
    #         noti = Notification.objects.filter(
    #             id=pk,
    #             user_id=user_header,
    #             is_deleted=False
    #         ).order_by('-created_at').first()

    #         if not noti:
    #             return custom_response(400, "Invalid Notification", [])

    #         noti.is_seen = datetime.utcnow()
    #         noti.save()

    #         return custom_response(200, "Seen notification successfully")
    #     except Exception as e:
    #         logger.info(f"EXCEPTION: seen_notification ----------{str(e)}")
    #         return custom_response(500, constants.RESP_MSG_ERROR_IN_SERVER)

    # @action(detail=False, methods=["POST"], url_path="seen-all-notifications")
    # def seen_all_notifications(self, request):
    #     try:
    #         user_header = get_user_from_header(request.headers)
    #         Notification.objects.filter(
    #             user_id=user_header,
    #             is_deleted=False,
    #             is_seen__isnull=True
    #         ).update(is_seen=datetime.utcnow())

    #         return custom_response(200, "Seen all notifications successfully")
    #     except Exception as e:
    #         logger.info(f"EXCEPTION: seen_notification ----------{str(e)}")
    #         return custom_response(500, constants.RESP_MSG_ERROR_IN_SERVER)

    @action(detail=False, methods=["POST"], url_path="users")
    def users(self, request):
        try:
            sz = RegisterCalendarTokenSerializer(data=request.data)
            if sz.is_valid(raise_exception=True):
                user_header = get_email_from_header(request.headers)

                User.objects.update_or_create(
                    email=user_header,
                    defaults={
                        'calendar_access_token': sz.data.get('calendar_access_token'),
                        'calendar_refresh_token': sz.data.get('calendar_refresh_token'),
                        'client_id': sz.data.get('client_id'),
                        'client_secret': sz.data.get('client_secret'),
                    }
                )
            return custom_response(200, "Save Calendar Token Successfully")
        except Exception as e:
            logger.info(f"EXCEPTION: register_token ----------{str(e)}")
            return custom_response(500, str(e))

    @action(detail=False, methods=["GET"], url_path="configs")
    def get_config(self, request):
        try:
            user_header = get_email_from_header(request.headers)

            user = User.objects.filter(
                email=user_header
            ).first()

            sz = UserSerializer(user)

            return custom_response(200, "Lấy danh sách calendar thành công.", sz.data)
        except Exception as e:
            logger.info(f"EXCEPTION: register_token ----------{str(e)}")
            return custom_response(500, str(e))

    @action(detail=False, methods=["POST"], url_path="save-configs")
    def update_config(self, request):
        try:
            user_header = get_email_from_header(request.headers)

            User.objects.update_or_create(
                email=user_header,
                defaults={
                    'is_web_noti': request.data.get('is_web_noti'),
                    'is_workplace_noti': request.data.get('is_workplace_noti'),
                    'is_discord_noti': request.data.get('is_discord_noti'),
                }
            )
            return custom_response(200, "Save Calendar Token Successfully")
        except Exception as e:
            logger.info(f"EXCEPTION: register_token ----------{str(e)}")
            return custom_response(500, str(e))


    @action(detail=False, methods=["POST"], url_path="register-token")
    def register_token(self, request):
        try:
            sz = RegisterTokenSerializer(data=request.data)
            if sz.is_valid(raise_exception=True):
                user_header = get_email_from_header(request.headers)

                FCMDevice.objects.filter(name=user_header).delete()
                FCMDevice.objects.filter(registration_id=sz.data.get('token')).delete()

                FCMDevice.objects.create(
                    name=user_header,
                    registration_id=sz.data.get('token'),
                    type='web'
                )
            return custom_response(200, "Save Firebase Token Successfully")
        except Exception as e:
            logger.info(f"EXCEPTION: register_token ----------{str(e)}")
            return custom_response(500, str(e))

    # @action(detail=True, methods=["GET"], url_path="fcm")
    # def fcm(self, request, pk=None):
    #     try:
    #         return render(request, 'index.html')
    #     except Exception as e:
    #         logger.info(f"EXCEPTION: fcm ----------{str(e)}")
    #         return custom_response(500, constants.RESP_MSG_ERROR_IN_SERVER)

    @action(detail=False, methods=["GET"], url_path="send-noti")
    def send_noti(self, request):
        try:
            user_header = get_email_from_header(request.headers)
            device = FCMDevice.objects.filter(name=user_header).first()
            if not device:
                print(f"Not found FCMDevice for user_header: {user_header}")
                return custom_response(400, f"Not found FCMDevice for user_header: {user_header}")

            noti = Notification.objects.filter(user__email=user_header).first()

            sz = GetNotificationSerializer(noti)

            device.send_message(
                messaging.Message(
                    data=sz.data
                )
            )

            return custom_response(200, "Successfully sent message")
        except Exception as e:
            logger.exception(f"EXCEPTION: send_noti ----------{str(e)}")
            return custom_response(500, str(e))


    @action(detail=False, methods=["GET"], url_path="calendar-crawler")
    def get_calendar(self, request):
        try:
            user_header = get_email_from_header(request.headers)
            user= User.objects.get(email=user_header)
            abc = "Bearer ya29.a0AfB_byC4c6bf0BSOfxBTJ0y16c_OfYn8Hj9rkzlIk_fZkQCrST4s32MeHasVjEEnGgRzp9cQy-F92MksWG_ptPAk8-DeCEop_ALCa6LLmMqz7xUfNhizcouCwei4FaTeHEyvD8vArcAWCWNxhA1FswLc_fDvoW_-z810aCgYKAXISARASFQGOcNnC7IugAgcFxYX4_9vRj8cAbg0171"

            headers = {"Authorization": abc}
            # headers = {"Authorization": f"Bearer {user.calendar_token}"}
            from_time = '2023-10-31T23:59:59%2B07:00'
            to_time = '2023-10-01T00:00:00%2B07:00'
            url = f'https://www.googleapis.com/calendar/v3/calendars/{user.email}/events?timeMax={from_time}&timeMin={to_time}'
            x = requests.get(url, headers=headers)

            if x.status_code != 200:
                return custom_response(x.status_code, x.text)

            calendar_lst = x.json()
            for item in calendar_lst.get('items'):
                if not item.get('summary'):
                    continue
                
                if Notification.objects.filter(id=item.get('id')).first():
                    break

                Notification.objects.create(
                    id=item.get('id'),
                    user=user,
                    creator=item.get('creator', {}).get('email'),
                    summary=item.get('summary'),
                    location=item.get('location'),
                    htmlLink=item.get('htmlLink'),
                    start=item.get('start', {}).get('dateTime'),
                    end=item.get('end', {}).get('dateTime')
                )

                print(item.get('summary'))
                print(item.get('creator', {}).get('email'))
                print(item.get('location'))
                print(item.get('htmlLink'))
                print(item.get('start', {}).get('dateTime'))
                print(item.get('end', {}).get('dateTime'))
                print("=" * 100)

            return custom_response(200, "Successfully sent message")
        except Exception as e:
            logger.exception(f"EXCEPTION: send_noti ----------{str(e)}")
            return custom_response(500, str(e))

    
    @action(detail=False, methods=["GET"], url_path="calendar-trigger")
    def calendar_trigger(self, request):
        try:
            print("heheheh")
            
            # sz_data = {}

            # send_notification_to_workchat('dunt14@fpt.com', f"""
            #     CALENDAR\nSummary: Hello \nCreator: {sz_data.get('creator')} \nLocation: {sz_data.get('location')} \nHtmlLink: {sz_data.get('htmlLink')} \nStart: {sz_data.get('start')} \nEnd: {sz_data.get('end')}\n
            # """)



            check_calender()

            # new_crond = CrontabSchedule.objects.create(
            #     # minute='*/15',
            #     hour='*',
            #     day_of_week='*',
            #     day_of_month='*',
            #     month_of_year='*',
            # )
            # periodic_task = PeriodicTask.objects.create(
            #     crontab=new_crond,
            #     name='Update Calendar',
            #     task='update_calender',
            # )

            # print(f'crseated {periodic_task=}')
            return custom_response(200, "Successfully sent message")
        except Exception as e:
            logger.exception(f"EXCEPTION: send_noti ----------{str(e)}")
            return custom_response(500, str(e))
