# -*- coding: utf-8 -*-

NATS_CLIENT_NAME_DEFAULT = 0
NATS_CLIENT_NAME_SUBSCRIBE_ONLY = 1


#
# LEGACY CHATWS
#

# -------------------------------------------------------------------
# ChatWs <-----------> CoreChat
CORECHAT_TO_CHATWS_FACEBOOK = 'CoreChat.To.ChatWs.FaceBook.{room_id}'
CORECHAT_TO_CHATWS_LIVECHAT = 'CoreChat.To.ChatWs.FChat.{room_id}'
CORECHAT_TO_CHATWS_ZALO = 'CoreChat.To.ChatWs.Zalo.{room_id}'
# --------End--------------------------------------------------------


# -------------------------------------------------------------------
# Celery worker <-----------> CoreChat
REMINDER_CHAT_SERVICE_TO_WEBSOCKET = "reminder.ChatService.To.WebSocket.{room_id}"  # REMINDER FOR ROOM
# --------End--------------------------------------------------------


# -------------------------------------------------------------------
# ChatWs <-----------> CoreChat
REOPEN_CORECHAT_TO_WEBSOCKET = "UpdateRoom.CoreChat.To.Websocket.{room_id}"  # REOPEN CHAT FOR ROOM
FOLLOW_CORECHAT_TO_WEBSOCKET = "CoreChat.To.Websocket.Follow.{room_id}"
NEW_ROOM_CORECHAT_TO_WEBSOCKET = 'CoreChat.To.Websocket.NewRoom.{room_id}'  # New Room Info
# --------End--------------------------------------------------------


#
# LEGACY WEBHOOK
#

# -------------------------------------------------------------------
# Webhook <-----------> CoreChat
CHAT_SERVICE_TO_CORECHAT_SUBSCRIBE = "ChatService.To.CoreChat.*"
WEBHOOK_TO_CORECHAT_MESSAGE = 'Webhook.To.CoreChat.Message.{page_id}'       # messsage send from webhook to core chat
# messsage send from CORECHAT to WEBHOOK LIVECHAT ANONYMOUS
CORECHAT_TO_WEBHOOK_LIVECHAT = "CoreChat.To.Webhook.FChat.{page_id}"
# --------End--------------------------------------------------------


# -------------------------------------------------------------------
# ChatWs <-----------> CoreChat
CORECHAT_TO_WEBSOCKET_FACEBOOK = "CoreChat.To.ChatWs.FaceBook.{page_id}"   # CORECHAT OF OMNICHAT SERVICE -> WS FACEBOOK
CORECHAT_TO_WEBSOCKET_LIVECHAT = "CoreChat.To.ChatWs.FChat.{page_id}"   # CORECHAT OF OMNICHAT SERVICE -> WS LIVECHAT
CORECHAT_TO_WEBSOCKET_ZALO = "CoreChat.To.ChatWs.Zalo.{page_id}"   # CORECHAT OF OMNICHAT SERVICE -> WS ZALO
# --------End--------------------------------------------------------


# message type
NATS_MSG_TYPE_TEXT = "text"
NATS_MSG_TYPE_FOLLOW = "follow"
NATS_MSG_TYPE_UNFOLLOW = "unfollow"
NATS_MSG_TYPE_LEAVE_LIVECHAT_LOG = "leave-livechat-log"


# -------------------------------------------------------------------
# ChatWs <-----------> Webhook
CHATWS_TO_WEBHOOK_LIVECHAT = "ChatWs.To.Webhook.FChat.{page_id}"   # CORECHAT OF OMNICHAT SERVICE -> WS FACEBOOK
# --------End--------------------------------------------------------


#
# NEW
#
CORECHAT_TO_CHATWS_CHAT_MSG = 'CoreChat.To.ChatWs.ChatMsg.{chat_type}.{room_id}'
CORECHAT_TO_CHATWS_CHAT_CONTROL = 'CoreChat.To.ChatWs.ChatControl.{chat_type}.{room_id}'

CORECHAT_TO_WEBHOOK_CHAT_MSG = 'CoreChat.To.Webhook.ChatMsg.{chat_type}.{room_id}'
CORECHAT_TO_WEBHOOK_CHAT_CONTROL = 'CoreChat.To.Webhook.ChatControl.{chat_type}.{room_id}'


CHAT_SERVICE_TO_CORECHAT_PUBLISH = "ChatService.To.CoreChat"
UPDATE_ROOM_CHAT_SERVICE_TO_WEBSOCKET = 'UpdateRoom.CoreChat.To.Websocket'  # Update status of room
CORECHAT_TO_REPORT_WORKER_PUBLISH = "CoreChat.To.ReportWorker"
CORECHAT_TO_REPORT_WORKER_SUBSCRIBE = "CoreChat.To.ReportWorker.*"      # CORECHAT    --> REPORT WORKER <Subscribe>

CORECHAT_TO_WEBSOCKET_NEW_ROOM = 'CoreChat.To.Websocket.NewRoom'  # New Room Info


# -----------------------------------------------
#    CORE CHAT    >>>>>>>>>>>   WEBHOOK
#           (fchat ack, user_log)
NATS_SUBJECT_CORECHAT_TO_WEBHOOK_WS_CLIENT = 'CoreChat.To.Webhook.WsClient.{chat_type}.{room_id}'
NATS_SUBJECT_CORECHAT_TO_CHATWS_WS_CLIENT = 'CoreChat.To.ChatWs.WsClient.{chat_type}.{room_id}'


# -----------------------------------------------
#    WEBHOOK    >>>>>>>>>>>   CORECHAT
#  (chat_msg, user_log, chat_action_event)
NATS_SUBJECT_WEBHOOK_TO_CORECHAT_CHAT_MESSAGE = 'Webhook.To.CoreChat.Message.{page_id}'
