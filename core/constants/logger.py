# -*- coding: utf-8 -*-
import json
import os
from typing import Dict

LOGGER = 'logger'
CONSOLE_LOGGER = 'sop-console'
REDIS_LISENER_CONSOLE_LOGGER = 'redis-listener'
DEBUG_LOGGER = 'sop-debug'
DJANGO_SERVER_LOGGER = 'django.server'


def add_extra_logger(default: Dict, **kwargs):
    if not default or not isinstance(default, dict):
        default = {}
    if kwargs:
        default.update(kwargs)
    return default


LOG_ACTION_CREATE_CUSTOMER_JOURNEY = 'create-customer-journey'
LOG_ACTION_PUSH_ELK = 'push-elk'
LOG_ACTION_ZALO_CHANGE_FORWARD_CHAT_SETTINGS = 'zalo-change-forward-settings'


LOG_EXTRA_PUSH_ELK = lambda **kwargs: add_extra_logger({        # noqa
    'chat-type': None,
    'story': None,
    'action': LOG_ACTION_PUSH_ELK,
    'room_id': None,
    'location': None,
    'data': None
}, **kwargs)


LOG_EXTRA_ZALO_FORWARD_CHAT = lambda **kwargs: add_extra_logger({       # noqa
    'chat-type': 'zalo',
    'story': 'forward-chat',
    'action': LOG_ACTION_ZALO_CHANGE_FORWARD_CHAT_SETTINGS,
    'room_id': None,
    'location': None,
    'data': None
}, **kwargs)


LOG_EXTRA_ZALO_ASSIGN_CHAT = lambda **kwargs: add_extra_logger({        # noqa
    'chat-type': 'zalo',
    'story': 'assign-chat',
    'action': None,
    'room_id': None,
    'location': None,
    'data': None
}, **kwargs)


LOG_COMPONENT_API = 'api'
LOG_COMPONENT_CELERY_TASK = 'celery-task'
LOG_COMPONENT_RABBITMQ_CONSUMER = 'rabbitmq-consumer'
LOG_COMPONENT_WEBHOOK = 'webhook'


LOG_CHAT_TYPE_ZALO = 'zalo'
LOG_CHAT_TYPE_FACEBOOK = 'facebook'
LOG_CHAT_TYPE_FCHAT = 'fchat'


LOG_FEAT_CONNECT_CHAT = 'connect-chat'
LOG_FEAT_CONFIG_FCHAT = 'config-fchat'
LOG_FEAT_HANDLE_WEBHOOK_MSG = 'handle-webhook-message'
LOG_FEATURE_SEND_MSG = 'send-message'
LOG_FEAT_SEEN_MSG = 'seen-message'
LOG_FEAT_MSG_REACTION = 'message-reaction'
LOG_FEAT_SYNC_MSG = 'sync-message'
LOG_FEAT_CONFIG_CHAT_DISTRIBUTION = 'config-chat-distribution'
LOG_FEAT_DISTRIBUTE_CHAT = 'distribute-chat'
LOG_FEAT_ASSIGN_CHAT = 'assign-chat'
LOG_FEAT_SEND_NOTI = 'send-noti'
LOG_FEAT_SEND_NOTI_WEB = 'send-noti-web'
LOG_FEAT_SEND_NOTI_MOBILE = 'send-noti-mobile'
LOG_FEAT_CHECK_PAGE_ACCESS_TOKEN = 'check-page-access-token'
LOG_FEAT_CUSTOMER_JOURNEY = 'customer-journey'
LOG_FEAT_COMPLETE_ROOM = 'complete-room'
LOG_FEAT_REOPEN_ROOM = 'reopen-room'
LOG_FEAT_REMIND_ROOM = 'remind-room'
LOG_FEAT_CUSTOMER_FOLLOW_PAGE = 'customer-follow-page'

LOG_ACTION_PUBLISH_RABBIT_MQ = 'publish-rabbitmq'
LOG_ACTION_CONSUME_RABBIT_MQ = 'consume-rabbitmq'


ALLOW_CUSTOM_EXTRA_FROM_KWARGS = (
    'chat-type',
    'feature',
    'component',
    'action',

    'room_id',
    'user_id',
    'fanpage_id',
    'customer_id',
    'mid',

    'method',
    'url_path',
    'headers',
    'status_code',
    'file_type',
    'file_size',

    'exchange',
    'routing_key',
    'rabbit_publish_data',
    'rabbit_publish_result',
    'rabbit_consumer_data',
    'rabbit_consumer_message',
)

LOG_CHAT_TYPES = {  # add more chat types here
    'zl': LOG_CHAT_TYPE_ZALO,
    'fb': LOG_CHAT_TYPE_FACEBOOK,
    'fc': LOG_CHAT_TYPE_FCHAT,
}


LOG_FEATS = {  # add more features here
    '10': LOG_FEAT_CONNECT_CHAT,
    '11': LOG_FEAT_CONFIG_FCHAT,
    '12': LOG_FEAT_HANDLE_WEBHOOK_MSG,
    '13': LOG_FEATURE_SEND_MSG,
    '14': LOG_FEAT_SEEN_MSG,
    '15': LOG_FEAT_MSG_REACTION,
    '16': LOG_FEAT_SYNC_MSG,
    '17': LOG_FEAT_CONFIG_CHAT_DISTRIBUTION,
    '18': LOG_FEAT_DISTRIBUTE_CHAT,
    '19': LOG_FEAT_ASSIGN_CHAT,
    '20': LOG_FEAT_SEND_NOTI,
    '21': LOG_FEAT_SEND_NOTI_WEB,
    '22': LOG_FEAT_SEND_NOTI_MOBILE,
    '23': LOG_FEAT_CHECK_PAGE_ACCESS_TOKEN,
    '24': LOG_FEAT_CUSTOMER_JOURNEY,
    '25': LOG_FEAT_COMPLETE_ROOM,
    '26': LOG_FEAT_REOPEN_ROOM,
    '27': LOG_FEAT_REMIND_ROOM,
    '28': LOG_FEAT_CUSTOMER_FOLLOW_PAGE,
}

LOG_COMPONENTS = {  # add more components here
    'api': LOG_COMPONENT_API,
    'ctk': LOG_COMPONENT_CELERY_TASK,
    'rmq': LOG_COMPONENT_RABBITMQ_CONSUMER,
    'whk': LOG_COMPONENT_WEBHOOK,
}

LOG_ACTIONS = {  # add more actions here
    '10': LOG_ACTION_PUBLISH_RABBIT_MQ,
    '11': LOG_ACTION_CONSUME_RABBIT_MQ
}

# code defination
# <chat-type>.<feature>.<component>.<action>
# code depend on order added in LOG_CODE
#
# Do NOT CHANGE THIS BELLOW CODE
#
LOG_CODES = {}
for chat_type_code, chat_type in LOG_CHAT_TYPES.items():
    for feat_code, feat in LOG_FEATS.items():
        for component_code, component in LOG_COMPONENTS.items():
            for action_code, action in LOG_ACTIONS.items():
                code = f"{chat_type_code}.{feat_code}.{component_code}.{action_code}"
                LOG_CODES[code] = {
                    'chat-type': chat_type,
                    'feature': feat,
                    'component': component,
                    'action': action,
                }

with open(os.path.join(os.getcwd(), 'log_codes.json'), 'w') as f:
    json.dump(LOG_CODES, f, indent=4)
