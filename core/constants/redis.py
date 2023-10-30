# -*- coding: utf-8 -*-


REDIS_CLIENT_NAME_SYNC_CACHE = 100
REDIS_CLIENT_NAME_SUBSCRIBER = 'redis-subscriber-client'


REDIS_REPORT_CHAT_REPORT_SALEMAN_BY_TIMESTAMP = 'redis_report_chat_report_saleman_by_timestamp__'
REDIS_CHAT_ROOM_NEW_FEEDBACK = 'redis_chat_room_new_feedback__{page_id}__{external_id}'

REDIS_BROWSER_ORIGIN_BY_USER = 'redis_browser_origin_by_user__'
REDIS_SET_TIME_REFRESH_TOKEN_ZALO = 'redis_set_time_refresh_token_zalo__{page_id}'

REDIS_PUBSUB_FACEBOOK_MSG_TO_WS_CLIENT = 'facebook.message.{room_id}'
REDIS_PUBSUB_ZALO_MSG_TO_WS_CLIENT = 'zalo.message.{room_id}'
REDIS_PUBSUB_FCHAT_MSG_TO_WS_CLIENT = 'fchat.message.{room_id}'
REDIS_PUBSUB_CHAT_REMINDER = 'chat.reminder.{room_id}'

REDIS_QUOTA_IN_MONTH_ZALO_FOR_PAGE = 'redis_quota_in_month_zalo_for_pages'
REDIS_QUOTA_ZALO_IN_MONTH_FOR_PAGE_BY_PAGE_ID = 'quota_in_month_page_{page_id}'

REDIS_QUOTA_IN_48h_ZALO_FOR_PAGE = 'redis_quota_in_48h_zalo_for_page_{page_id}'
REDIS_QUOTA_IN_48H_ZALO_FOR_PAGE_MAPPING_EXTERNAL = 'redis_quota_in_48h_zalo_for_page_external_{external_id}'

REDIS_CHAT_ROOM_ZALO = "redis_chat_room_zalo__{room_id}"
