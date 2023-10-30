# -*- coding: utf-8 -*-
from typing import List, Optional

from core import constants
from core.abstractions import CustomBaseModel
from pydantic import BaseModel


class CoreChatInputMessage(BaseModel):
    msg_type: str
    chat_type: str


class SendMessageAttachment(CustomBaseModel):
    id: Optional[str]
    type: Optional[str]
    url: Optional[str]
    name: Optional[str]
    size: Optional[str]
    video_url: Optional[str]


class LogMessageSchema(CustomBaseModel):
    log_type: Optional[str]
    message: Optional[str]
    room_id: Optional[str]
    from_user: Optional[str]
    to_user: Optional[str]
    created_at: Optional[str]


class NatsSalemanMsgModel(CustomBaseModel):
    mid: Optional[str]
    attachments: List[SendMessageAttachment] = []
    text: Optional[str] = None
    created_time: Optional[str]
    sender_id: Optional[str]
    recipient_id: Optional[str]
    error_message: Optional[int] = None
    room_id: Optional[str]
    is_sender: bool = False
    created_at: str
    is_seen: Optional[str]
    message_reply: Optional[str]
    reaction: Optional[str] = None
    reply_id: Optional[str] = None
    sender_name: Optional[str] = None
    uuid: Optional[str]
    msg_status: Optional[str] = 'send_message-status'
    type: Optional[str] = constants.CHAT_TYPE_FACEBOOK
    user_id: List[str] = []
    event: Optional[str]
    is_log_msg: Optional[bool] = False
    log_message: Optional[LogMessageSchema] = None

    # for new
    route_type: Optional[str] = 'chat'
    chat_type: Optional[str] = None  # for finding chat manager get from typeChat for fit old version
    msg_type: Optional[str] = None  # for finding core router get from typeMessage for fit old version
