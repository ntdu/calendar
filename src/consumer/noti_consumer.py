# -*- coding: utf-8 -*-
import logging

from core import constants
from django.core.cache import cache
from fcm_django.models import FCMDevice
from firebase_admin import messaging
from src.dj_project.service_settings import service_settings
from src.notification.models import Notification, User
from src.notification.serializers import NotificationSerializer
from src.notification.tasks import merge_noti_task
from src.notification.utils import get_token, send_notification_to_isc

logger = logging.getLogger(constants.CONSOLE_LOGGER)


# def noti_callback_handler(body, *args):     # NOSONAR
#     print("body noti_callback_handler =============", body)
#     """
#     This function handles incoming messages from Facebook Webhook, creates or updates chat rooms, stores
#     messages, and sends messages to WebSocket clients.

#     :param body: The body parameter is the message body received from the Facebook webhook. It is passed
#     as an argument to the message_callback_handler function
#     :return: The function does not explicitly return anything, but it may return an error message as a
#     string if an exception is caught.
#     """

#     MSG_PATTERN_SETTINGS = {
#         'CHAT': {
#             'NEW_ROOM': {
#                 'message': '{customer_name} đã gửi tin nhắn mới đến bạn',
#                 'link': 'chat/{room_id}',        # NOSONAR
#                 'is_redirect': True
#             },
#             'ASSIGN': {
#                 'message': '{user_name} đã chỉ định chat với khách hàng {customer_name} cho bạn',
#                 'link': 'chat/{room_id}',        # NOSONAR
#                 'is_redirect': True
#             },
#             'USER_REPLY': {
#                 'message': 'Bạn vẫn chưa phản hồi khách hàng {customer_name}',
#                 'link': 'chat/{room_id}',        # NOSONAR
#                 'is_redirect': True
#             },
#             'NEW_MESSAGE': {
#                 'message': '{customer_name}{extras}',
#                 'link': 'chat/{room_id}',        # NOSONAR
#                 'is_redirect': True
#             }
#         },
#         'REMINDER': {
#             'REMINDER': {
#                 'message': 'Nhắc nhở: {extras}',
#                 'link': 'chat/{room_id}',        # NOSONAR
#                 'is_redirect': True
#             }
#         },
#         'FEEDBACK': {
#             'FEEDBACK': {
#                 'message': 'Bạn có feedback mới từ {customer_name}',
#                 'link': 'chat',
#                 'is_redirect': False
#             }
#         },
#         'SETTING': {
#             'DISCONNECTED': {
#                 'message': 'Bạn vừa bị mất kết nối với kênh {extras}. Vui lòng kết nối lại!',
#                 'link': 'chat',
#                 'is_redirect': False
#             },
#             'UPDATE_ROLE': {
#                 'message': '{user_name} đã cập nhật vai trò {extras} cho bạn',
#                 'link': 'chat',
#                 'is_redirect': False
#             }
#         }
#     }

#     try:
#         sz = NotificationSerializer(data=body)
#         users, data = sz.validate(body)
#         for item in users:
#             user_id = item.get('user_id')
#             emp_id = item.get('emp_id')

#             user, created = User.objects.get_or_create(     # noqa  # NOSONAR
#                 user_id=user_id,
#                 defaults={'emp_id': emp_id}
#             )

#             if data.get('subtype') != 'NEW_MESSAGE':
#                 user.unsent_noti_count += 1
#                 user.save()

#             noti = Notification.objects.create(
#                 user=user,
#                 room_id=data.get('room_id'),
#                 channel=data.get('channel'),
#                 type=data.get('type'),
#                 subtype=data.get('subtype'),
#                 user_name=data.get('user_name'),
#                 avatar=data.get('avatar'),
#                 customer_name=data.get('customer_name'),
#                 extras=data.get('extras')
#             )

#             if (noti.type == 'CHAT' and (
#                 noti.subtype == 'NEW_ROOM' or noti.subtype == 'USER_REPLY'
#             )) or noti.type == 'FEEDBACK':
#                 merge_noti_task.apply_async((noti.id,), countdown=30)

#             data['id'] = str(noti.id)
#             data['type_signal'] = 'MESSAGING'
#             data['created_at'] = str(noti.created_at)

#             # Push notifications to Firebase
#             device = FCMDevice.objects.filter(name=user_id).first()
#             if device:
#                 device.send_message(
#                     messaging.Message(
#                         data=data
#                     )
#                 )

#                 logger.warning(f"Send noti successfully for user_id: {user_id}")
#             else:
#                 logger.warning(f"Not found FCMDevice for user_id: {user_id}")

#             # Push notifications to mobile
#             if not emp_id:
#                 continue

#             msg_pattern_by_type = MSG_PATTERN_SETTINGS.get(data.get('type'))

#             if not msg_pattern_by_type:
#                 # print("MSG_PATTERN_SETTINGS:", MSG_PATTERN_SETTINGS)
#                 logger.warning(f"Not found {MSG_PATTERN_SETTINGS=} for type: {data.get('type')}")
#                 return

#             msg_pattern_by_type = msg_pattern_by_type.get(data.get('subtype'))
#             if not msg_pattern_by_type:
#                 print("MSG_PATTERN_SETTINGS:", MSG_PATTERN_SETTINGS)
#                 print("Not found msg_pattern_by_type for subtype:", data.get('subtype'))
#                 return

#             message = msg_pattern_by_type.get('message').format(
#                 user_name=data.get('user_name'),
#                 customer_name=data.get('customer_name'),
#                 extras=data.get('extras')
#             )
#             link = msg_pattern_by_type.get('link').format(
#                 room_id=data.get('room_id'),
#             )

#             logger.info(f"ISC link: {link}")
#             cached_access_token_value = cache.get('access_token')
#             if not cached_access_token_value:
#                 response = get_token(service_settings.SERVICE_ISC_ISC_USERNAME,
#                                      service_settings.SERVICE_ISC_ISC_PASSWORD)

#                 if response and response.get('Code') == 200:
#                     rsp_data = response.get('Data')
#                     access_token = rsp_data.get('AccessToken')
#                     timeout = rsp_data.get('AccessTokenLifeTime') - 600

#                     cache.set('access_token', access_token, timeout=timeout)
#                     cached_access_token_value = access_token
#                 else:
#                     print('Request failed with status code:', response.status_code)

#             isc_data = {
#                 "Title": "SOP",
#                 "Message": message,
#                 "BackLink": link,
#                 "IsRedirect": msg_pattern_by_type.get('is_redirect'),
#                 "PSId": emp_id
#             }
#             response = send_notification_to_isc(access_token=cached_access_token_value, data=isc_data)
#             if response.get('Code') == 401:
#                 logger.warn(f'send notification to ISC get 401 {isc_data=}')

#             print("isc: ", response)

#     except Exception as e:
#         logger.exception(f"noti_callback_handler get exception {e}")
