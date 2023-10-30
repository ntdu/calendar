# -*- coding: utf-8 -*-

FCHAT_UPLOAD_FILE_TYPES = (
    'doc', 'docx',
    'xls', 'xlsx',
    'ppt', 'pptx',
    'pdf',
    'png',
    'jpg', 'jpeg',
    'mp3', 'mp4', 'wav', 'wma', 'flac',
    'video/x-ms-wma',
    'audio/wav',
    'zip', 'rar'
)

FCHAT_UPLOAD_FILE_TYPE_MAPPING = {
    'application/x-zip-compressed': '.zip',
    'application/vnd-rar': '.rar',
    'application/vnd.rar': '.rar',
}


FCHAT_EVENT_NEW_MESSAGE = 'new-message'
FCHAT_EVENT_CUSTOMER_LEVEAVE_ROOM = 'customer-leave-room'
FCHAT_EVENT_CUSTOMER_START_NEW_ROOM = 'customer-start-room'
LIVECHAT_ROOM_MINIO = "livechat_room"


# US #1748 Fchat default survey
REGEX_PHONE = r'^(0([0-9]){7,11})$|(^\+84)([0-9]{5,9})$'
REGEX_EMAIL = r'^[a-zA-Z0-9][a-zA-Z0-9\._+-]*@([a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]{0,})+([a-zA-Z0-9_-][a-zA-Z0-9_-]{0,})+$'
