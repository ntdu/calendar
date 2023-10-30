# -*- coding: utf-8 -*-

ROUTE_TYPE_CHAT = 'chat'


MANAGER_TYPE_WEBHOOK_CHAT_MESSAGE = 'manager-type-webhook-chat-message'
MANAGER_TYPE_SALESMAN_SEND_MESSAGE = 'manager-type-salesman-send-message'
MANAGER_TYPE_USER_CHAT_LOG = 'manager-type-salesman-chat-logs'
MANAGER_TYPE_CHAT_ACTIONS = 'manager-type-chat-actions'
MANAGER_TYPE_REPORT_ADMIN = 'manager-type-report-admin'
MANAGER_TYPE_REPORT_SALEMAN = 'manager-type-report-saleman'


CHAT_TYPE_FACEBOOK = 'facebook'
CHAT_TYPE_ZALO = 'zalo'
CHAT_TYPE_LIVECHAT = 'livechat'
CHAT_TYPE_FCHAT = 'fchat'
CHAT_TYPE_ALL = 'all'

MSG_TYPE_TEXT = 'text'
MSG_TYPE_NEW_SALESMAN_MSG = 'send_message-status'
MSG_TYPE_CHAT_LOG = 'chat-log'
MSG_TYPE_CHAT_ACTION = 'chat-actions'

MSG_TYPE_CHAT_EVENT_FOLLOW = 'follow'
MSG_TYPE_CHAT_EVENT_UNFOLLOW = 'unfollow'
MSG_TYPE_CHAT_EVENT_ZALO_OA_SEND_TEXT = 'oa_send_text'

CHAT_CONNECTOR_TYPE_FACEBOOK = CHAT_TYPE_FACEBOOK
CHAT_CONNECTOR_TYPE_ZALO = CHAT_TYPE_ZALO
CHAT_CONNECTOR_TYPE_FCHAT = CHAT_TYPE_FCHAT
CHAT_CONNECTOR_TYPE_LOCAL_SERVICE = 'local-service'


HANDLER_TYPE_WEBHOOK_MSG_FIND_DB_INFO = 'handler-type-webhook-message-find-db-info'
HANDLER_TYPE_WEBHOOK_MSG_GET_MSG_DETAIL = 'handler-type-webhook-message-get-msg-detail'
HANDLER_TYPE_WEBHOOK_MSG_STORAGE_MSG = 'handler-type-webhook-message-storage-msg'
HANDLER_TYPE_WEBHOOK_MSG_STORAGE_REDIS = 'handler-type-webhook-message-storage-redis'
HANDLER_TYPE_WEBHOOK_MSG_NOTIFY_WS_NEW_ROOM = 'handler-type-webhook-message-notify-ws-new-room'
HANDLER_TYPE_WEBHOOK_MSG_SEND_MSG_TO_WS_CLIENT = 'handler-type-webhook-message-send-to-websocket-client'
HANDLER_TYPE_WEBHOOK_MSG_SEND_TO_REPORT_WORKER = 'handler-type-webhook-message-send-to-report-worker'


HANDLER_TYPE_SALESMAN_MSG_STORAGE_MSG = 'handler-type-salesman-storage-msg'
HANDLER_TYPE_SALESMAN_MSG_SEND_TO_WEBSOCKET_CLIENT = 'handler-type-salesman-message-send-to-websocket-client'
HANDLER_TYPE_SALESMAN_MSG_SEND_TO_REPORT_WORKER = 'handler-type-salesman-message-send-to-report-worker'
HANDLER_TYPE_SALESMAN_MSG_COLLECT_LOG_CHAT = 'handler-type-salesman-message-collect-log-chat'


HANDLER_TYPE_USER_CHAT_LOG_STORAGE_LOG = 'handler-type-user-chat-log-storage-logs'
HANDLER_TYPE_USER_CHAT_LOG_SEND_TO_WEBSOCKET_CLIENT = 'handler-type-user-chat-log-send-to-websocket-client'

HANDLER_TYPE_CHAT_ACTION_EVENT = 'handler-type-chat-action-event'
HANDLER_TYPE_CHAT_ACTION_FIND_DB_INFO = 'handler-type-chat-action-find-db-info'

# Log message
CHAT_LOG_COMPLETED = 'have completed the conversation'
CHAT_LOG_NEW_MESSAGE = 'new message to'
CHAT_LOG_REOPENED = 'have reopened the conversation'
CHAT_LOG_REMINDED = 'has set up reminder'
CHAT_LOG_LEAVE_LIVECHAT = 'have left the conversation'
CHAT_LOG_FORWARDED = 'has forwarded the message to'
CHAT_LOG_NEW_MESSAGE_INTERACTION = 'has new interaction'
CHAT_LOG_ASSIGN_UNASSIGN_OAZALO = '{} zaloOA successfully'

CHAT_TRIGGER_NEW_MESSAGE = "new_message"
CHAT_TRIGGER_COMPLETED = 'completed'
CHAT_TRIGGER_REOPENED = 'reopen'
CHAT_TRIGGER_REMINDED = 'reminder'
CHAT_TRIGGER_LEFT_LEAVE_LIVECHAT = 'leave-livechat'
CHAT_TRIGGER_FORWARDED = 'forwarded'
CHAT_TRIGGER_NEW_MESSAGE_INTERACTION = 'new_interaction'
CHAT_TRIGGER_ASSIGN_UNASSIGN_ZALOOA = 'zaloOA'

CHAT_LOG_MESSAGE_ACK = 'Log.Message.ACK'


CHAT_ROOM_STATUS_ALL = 'all'
CHAT_ROOM_STATUS_PROCESSING = 'processing'
CHAT_ROOM_STATUS_COMPLETED = 'completed'
CHAT_ROOM_STATUS_EXPIRED = "expired"
CHAT_ROOM_STATUS_REOPENED = 'reopen'
SEND_MESSAGE_STATUS = "send_message-status"
SIO_EVENT_ACK_MSG_SALEMAN_TO_CUSTOMER = 'SaleMan.To.Customer.ACK'
FOLLOWER = 'follow'
CUSTOMER_TO_SALEMAN = 'Customer.To.SaleMan'
CUSTOMER_TO_SALEMAN_NEW_ROOM = 'Customer.To.SaleMan.NewRoom'
SIO_EVENT_ACK_ASSIGN_ROOM_CHAT = 'Assign.Room.Chat.ACK'

CHAT_SYNC_SIGNAL = 'sync_signal'    # socketio event to FE, # US #1728 FB. Đồng bộ tin nhắn
CHAT_ROOM_SEEN_MSG = 'seen_msg'    # US 43: Mark a seen message
CHAT_ROOM_REACTION_MSG = 'reaction_msg'  # US 44: Reaction a message

CHECK_FANPAGE_TOKEN = 'Check.Token.FanPage'
CHECK_FANPAGE_CONNECTION = 'Check.Connection.FanPage'

MESSAGE_REACTION_LIKE = 'like'
MESSAGE_REACTION_HAHA = 'haha'
MESSAGE_REACTION_LOVE = 'love'
MESSAGE_REACTION_WOW = 'wow'
MESSAGE_REACTION_SAD = 'sad'
MESSAGE_REACTION_ANGRY = 'angry'
MESSAGE_REACTION_YAY = 'yay'
MESSAGE_REACTION_REMOVE = 'remove'

MESSAGE_FACEBOOK_REACTION = {
    '/-heart': MESSAGE_REACTION_LOVE,
    ':>': MESSAGE_REACTION_HAHA,
    '/-strong': MESSAGE_REACTION_LIKE,
    ':o': MESSAGE_REACTION_WOW,
    ':-((': MESSAGE_REACTION_SAD,
    ':-h': MESSAGE_REACTION_ANGRY,
    '/-remove': MESSAGE_REACTION_REMOVE
}

MESSAGE_SOP_REACTION_FACEBOOK = {y: x for x, y in MESSAGE_FACEBOOK_REACTION.items()}
CACHE_REPLY = 'reply_log__'

FORMAT_HEIF = '.HEIF'
FORMAT_HEIF_LOWER = '.heif'
FORMAT_TIFF = '.TIFF'
FORMAT_TIFF_LOWER = '.tiff'
FORMAT_WEBP = '.WEBP'
FORMAT_WEBP_LOWER = '.webp'
FORMAT_GIF = '.GIF'
FORMAT_GIF_LOWER = '.gif'
FORMAT_JPG = '.JPG'
FORMAT_JPG_LOWER = '.jpg'
FORMAT_HEIC = '.HEIC'
FORMAT_HEIC_LOWER = '.heic'
FORMAT_TIF = '.TIF'
FORMAT_TIF_LOWER = '.tif'



FORMAT_NEED_CONVERT_TO_JPG = (
    FORMAT_HEIF,
    FORMAT_HEIF_LOWER,
    FORMAT_TIFF,
    FORMAT_TIFF_LOWER,
    FORMAT_WEBP,
    FORMAT_WEBP_LOWER,
    FORMAT_GIF,
    FORMAT_GIF_LOWER,
    FORMAT_JPG,
    FORMAT_JPG_LOWER,
    FORMAT_HEIC,
    FORMAT_HEIC_LOWER,
    FORMAT_TIF,
    FORMAT_TIF_LOWER
)
