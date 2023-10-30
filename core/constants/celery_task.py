# -*- coding: utf-8 -*-

NAMESPACE_DEFAULT = 'Celery'
IO_TASK = 'io_task'
CPU_TASK = 'cpu_task'

TASK_RESULT_BACKEND_DJANGO_DB = 'django-db'
TASK_RESULT_BACKEND_REDIS = 'redis'

QUEUE_IO_BOUND = 'io_bound'
QUEUE_CPU_BOUND = 'cpu_bound'


CELERY_TASK_VERIFY_INFORMATION = 'celery-task-verify-information'
CELERY_TASK_ASSIGN_CHAT = 'celery-task-assign-chat'

CELERY_TASK_REMINDER_ROOM = 'celery-task-reminder-room'

CELERY_TASK_LOG_MESSAGE_ROOM = "create-log-time-message"
CELERY_TASK_LOG_MESSAGE_REOPEN_ROOM = "create-log-message-reopen-room"

CELERY_TASK_STORAGE_MESSAGE_LIVECHAT = "storage-message-livechat"
CELERY_TASK_STORAGE_MESSAGE_FACEBOOK = "storage-message-facebook"
CELERY_TASK_STORAGE_MESSAGE_ZALO = "storage-message-zalo"


CELERY_TASK_COLLECT_LIVECHAT_SOCIAL_PROFILE = "collect_livechat_social_profile"
CELERY_TASK_UPDATE_PROFILE_USER_AFTER_FOLLOW_ZALO = "update_profile_user_after_follow_zalo"
CELERY_TASK_GET_CONTACT_FB_FAN_PAGE = 'get_contact_fb_fan_page'
CELERY_TASK_GET_CONTACT_ZALO_FAN_PAGE = 'get_contact_zalo_fan_page'

CELERY_TASK_WRITE_LOG_ELK = 'log_elk'


CELERY_TASK_RUN_REMINDER_MANAGEMENT_PROCESS = 'celery-task-run-reminder-management-process'
CELERY_TASK_REMIND_SALESMAN_CHECK_ROOM = 'celery-task-remind-salesman-check-room'

CELERY_TASK_REFRESH_TOKEN_OF_ZALOOA = 'celery_task_refresh_token_of_zalo'

CELERY_TASK_RUN_BLOCK_ROOM_SPAM = 'celery_task_run_block_room_spam'

CELERY_TASK_RECEIVE_FACEBOOK_MESSAGE_FROM_WEBHOOK = "celery-task-receive-facebook-msg-from-webhook"
CELERY_TASK_RECEIVE_ZALO_MESSAGE_FROM_WEBHOOK = "celery-task-receive-zalo-msg-from-webhook"
CELERY_TASK_RECEIVE_FCHAT_MESSAGE_FROM_WEBHOOK = "celery-task-receive-fchat-msg-from-webhook"
