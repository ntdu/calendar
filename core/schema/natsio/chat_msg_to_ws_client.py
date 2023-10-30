# -*- coding: utf-8 -*-

from typing import List, Optional

from core.abstractions import CustomBaseModel


class CmwAttachment(CustomBaseModel):
    name: Optional[str]
    type: Optional[str]
    url: Optional[str]
    video_url: Optional[str]
    size: Optional[str]


class CmwMessageServiceSurveyUserInfo(CustomBaseModel):
    title: Optional[str]
    value: Optional[str]


class CmwErrorMessageModel(CustomBaseModel):
    mid: Optional[str]
    code: Optional[str]
    type: Optional[str]
    message: Optional[str]
    url: Optional[str]


class CmwLogMessageDetail(CustomBaseModel):
    mid: Optional[str] = None
    log_type: Optional[str] = None
    message: Optional[str] = None
    room_id: Optional[str] = None
    from_user: Optional[str] = None
    to_user: Optional[str] = None
    created_at: Optional[str] = None


class ChatMessageToWsClient(CustomBaseModel):
    mid: Optional[str] = None
    room_id: Optional[str] = None
    attachments: List[CmwAttachment] = []
    service_survey: List[CmwMessageServiceSurveyUserInfo] = []
    created_at: Optional[str] = None
    is_seen: Optional[str]
    is_sender: bool = False
    message_reply: Optional[str] = None
    reaction: Optional[str] = None
    recipient_id: Optional[str] = None
    reply_id: Optional[str] = None
    sender_id: Optional[str]
    sender_name: Optional[str] = None
    text: Optional[str] = None
    uuid: Optional[str] = None
    created_time: Optional[str] = None
    event: Optional[str] = None
    user_id: Optional[List] = []
    timestamp: Optional[float] = None
    error_message: Optional[CmwErrorMessageModel] = None
    log_message: Optional[CmwLogMessageDetail] = None
