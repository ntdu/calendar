# -*- coding: utf-8 -*-
from typing import Dict, List, Optional

from core.abstractions import CustomBaseModel

from .base_pubsub import BaseNatsPubSubMessage


class NatsCustomerMsgAttachment(CustomBaseModel):
    name: Optional[str]
    type: Optional[str]
    payloadUrl: Optional[str]
    size: Optional[str]


class NatsCustomerMsgUserInfo(CustomBaseModel):
    title: Optional[str]
    value: Optional[str]


class NatsCustomerChatOptional(CustomBaseModel):
    chat_type: str
    data: Optional[Dict] = {}


class NatsCustomerLog(CustomBaseModel):
    log_type: Optional[str]
    message: Optional[str]
    room_id: Optional[str]
    from_user: Optional[str]
    to_user: Optional[str]
    created_at: Optional[str]


class NatsCustomerMsgModel(BaseNatsPubSubMessage):
    senderId: Optional[str]
    recipientId: Optional[str]
    timestamp: int
    text: Optional[str]
    mid: Optional[str]
    appId: str
    error_message: Optional[int] = None
    attachments: List[NatsCustomerMsgAttachment] = []
    user_info: List[NatsCustomerMsgUserInfo] = []
    typeChat: str
    typeMessage: Optional[str] = 'text'
    optionals: List[NatsCustomerChatOptional] = []
    uuid: Optional[str] = ""
    room_id: Optional[str] = None
    log_message: Optional[NatsCustomerLog] = None
    is_new_room: Optional[bool] = False                         # Check new room for log message
    is_new_chat: Optional[bool] = False                         # Check new chat
    is_new_conversation: Optional[bool] = False                 # Check new conversation for report saleman
    is_new_complete_conversation: Optional[bool] = False        # Check new conversation complete for report saleman
    new_feedback: Optional[bool] = False                        # New msg feedback - ex: Msg Fb/Zl/Fchat -> sale

    # for new
    route_type: Optional[str] = 'chat'
    chat_type: Optional[str] = None  # for finding chat manager get from typeChat for fit old version
    msg_type: Optional[str] = None  # for finding core router get from typeMessage for fit old version
