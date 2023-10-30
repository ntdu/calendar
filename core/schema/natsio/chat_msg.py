# -*- coding: utf-8 -*-
from typing import Dict, List, Optional

from core.abstractions import CustomBaseModel


class NatsChatMessageAttachment(CustomBaseModel):
    name: Optional[str]
    type: Optional[str]
    payloadUrl: Optional[str]
    size: Optional[str]


class NatsChatMessageUserInfo(CustomBaseModel):
    title: Optional[str]
    value: Optional[str]


class ChatOptional(CustomBaseModel):
    chat_type: str
    data: Optional[Dict] = {}


class LogMessageSchema(CustomBaseModel):
    log_type: Optional[str]
    message: Optional[str]
    room_id: Optional[str]
    from_user: Optional[str]
    to_user: Optional[str]
    created_at: Optional[str]


class NatsChatMessage(CustomBaseModel):
    senderId: Optional[str]
    recipientId: Optional[str]
    timestamp: int
    text: Optional[str]
    mid: Optional[str]
    appId: str
    error_message: Optional[int] = None
    attachments: List[NatsChatMessageAttachment] = []
    user_info: List[NatsChatMessageUserInfo] = []
    typeChat: str
    typeMessage: Optional[str] = 'text'
    optionals: List[ChatOptional] = []
    uuid: Optional[str] = ""
    room_id: Optional[str] = None
    log_message: Optional[LogMessageSchema] = None
    is_new_room: Optional[bool] = False                         # Check new room for log message
    is_new_chat: Optional[bool] = False                         # Check new chat
    is_new_conversation: Optional[bool] = False                 # Check new conversation for report saleman
    is_new_complete_conversation: Optional[bool] = False        # Check new conversation complete for report saleman
    new_feedback: Optional[bool] = False                        # New msg feedback - ex: Msg Fb/Zl/Fchat -> sale

    # for new
    route_type: Optional[str] = 'chat'
    manager_type: Optional[str] = None
    chat_type: Optional[str] = None  # for finding chat manager get from typeChat for fit old version
    msg_type: Optional[str] = None  # for finding core router get from typeMessage for fit old version
