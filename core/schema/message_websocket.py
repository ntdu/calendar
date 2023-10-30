# -*- coding: utf-8 -*-
from typing import Dict, List, Optional  # noqa

from core.abstractions import CustomBaseModel


class ChatMessageAttachment(CustomBaseModel):
    name: Optional[str]
    type: Optional[str]
    url: Optional[str]
    size: Optional[str]


class MessageServiceSurveyUserInfo(CustomBaseModel):
    title: Optional[str]
    value: Optional[str]


class MessageChat(CustomBaseModel):
    mid: Optional[str]
    room_id: Optional[str]
    attachments: List[ChatMessageAttachment] = []
    user_info: List[MessageServiceSurveyUserInfo] = []
    created_at: str
    is_seen: Optional[str]
    is_sender: bool = False
    message_reply: Optional[str]
    reaction: Optional[str] = None
    recipient_id: str
    reply_id: Optional[str] = None
    sender_id: str
    sender_name: Optional[str] = None
    text: Optional[str] = None
    uuid: Optional[str]
    created_time: Optional[str]
    event: Optional[str]
    user_id: Optional[str]
    timestamp: Optional[float]


class ErrorMessageModel(CustomBaseModel):
    mid: Optional[str]
    code: Optional[str]
    type: Optional[str]
    message: Optional[str]
    url: Optional[str]


class MessageToWebSocket(CustomBaseModel):
    mid: Optional[str]
    room_id: Optional[str]
    attachments: List[ChatMessageAttachment] = []
    service_survey: List[MessageServiceSurveyUserInfo] = []
    created_at: str
    is_seen: Optional[str]
    is_sender: bool = False
    message_reply: Optional[str]
    reaction: Optional[str] = None
    recipient_id: Optional[str] = None
    reply_id: Optional[str] = None
    sender_id: str
    sender_name: Optional[str] = None
    text: Optional[str] = None
    uuid: Optional[str]
    created_time: Optional[str]
    event: Optional[str]
    user_id: List[str] = []
    timestamp: Optional[float]
    error_message: Optional[ErrorMessageModel] = None


class CustomerInfo(CustomBaseModel):
    external_id: Optional[str]
    name: Optional[str]
    avatar: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]


class DataFollowToWebSocket(CustomBaseModel):
    room_id: Optional[str]
    user_info: Optional[CustomerInfo] = None
    event: Optional[str]
    user_id: List[str] = []
