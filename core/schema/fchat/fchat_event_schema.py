# -*- coding: utf-8 -*-
import time
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from core import constants
from core.abstractions import CustomBaseModel
from core.schema import (
    UclLogDetail,
    UserChatLog,
    WcmAttachment,
    WcmChatOptional,
    WebhookChatMessage,
)
from pydantic import validator


class FChatUserInfo(CustomBaseModel):
    title: str
    value: str


class FChatNewMessageAttachment(CustomBaseModel):
    type: Optional[str]
    payload_url: Optional[str]
    name: Optional[str]
    size: Optional[int]


class FChatWebhookEventMessage(CustomBaseModel):
    grid_total: int = 1
    grid_id: Optional[str] = None

    browser_origin: Optional[str] = None

    is_welcome_msg: bool = False
    is_text: bool = False
    is_sender: Optional[bool] = False
    client_id: str
    live_chat_id: str
    room_id: str
    message_text: Optional[str] = None
    file: Optional[bytes] = None
    file_type: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = 0
    request_id: Optional[str] = None
    attachments: List[FChatNewMessageAttachment] = []
    user_info: List[FChatUserInfo] = []

    @validator('file_name')
    def file_name_replace_space_by_underscore(cls, v):
        if isinstance(v, str):
            v = v[:50]
            v = v.replace(' ', '_')
            return ''.join(char for char in v if ord(char) < 128)
        return v

    @validator('request_id')
    def auto_request_id(cls, v):
        if isinstance(v, str):
            return v
        return str(uuid4())

    def convert_to_WebhookChatMessage(self) -> WebhookChatMessage:
        nats_attachments = []
        if self.attachments:
            for attachment in self.attachments:
                nats_attachments.append(
                    WcmAttachment(
                        type=attachment.type,
                        payloadUrl=attachment.payload_url,
                        name=attachment.name,
                        size=attachment.size
                    )
                )
        optionals = [
            WcmChatOptional(
                chat_type=constants.CHAT_TYPE_LIVECHAT,
                data={'is_sender': self.is_sender}
            )
        ]
        if self.user_info:
            optionals.append(
                WcmChatOptional(
                    chat_type=constants.CHAT_TYPE_LIVECHAT,
                    data={'user_info': self.user_info}
                )
            )
        if self.browser_origin:
            optionals.append(
                WcmChatOptional(
                    chat_type=constants.CHAT_TYPE_LIVECHAT,
                    data={'browser_origin': self.browser_origin}
                )
            )
        return WebhookChatMessage(
            is_sender=self.is_sender,
            sender_id=self.client_id,
            recipient_id=self.live_chat_id,
            timestamp=time.time(),
            text=self.message_text,
            mid=self.request_id,
            app_id="live-chat-app-id",
            attachments=nats_attachments,
            optionals=optionals,
            room_id=self.room_id,
            uuid=self.request_id if self.request_id else str(uuid4()),
            is_welcome_msg=self.is_welcome_msg
        )


class FChatWebhookNewRoomEventMessage(CustomBaseModel):
    client_id: str
    fchat_id: str
    room_id: str
    browser_origin: str

    def convert_to_WebhookChatMessage(self) -> WebhookChatMessage:
        return WebhookChatMessage(
            is_sender=True,
            sender_id=self.client_id,
            recipient_id=self.fchat_id,
            timestamp=time.time(),
            mid="",
            app_id="live-chat-app-id",
            optionals=[
                WcmChatOptional(
                    chat_type=constants.CHAT_TYPE_LIVECHAT,
                    data={'browser_origin': self.browser_origin}
                )
            ],
            room_id=self.room_id
        )


class FChatWebhookLeaveRoomEventMessage(CustomBaseModel):
    client_id: str
    fchat_id: str
    room_id: str

    def convert_to_UserChatLog(
        self,
        log_type: str = 'leave-livechat',
        log_msg: str = 'have left the conversation'
    ) -> UserChatLog:
        _time_now = str(datetime.now())
        return UserChatLog(
            text=log_msg,
            created_time=_time_now,
            sender_id=self.client_id,
            recipient_id=self.fchat_id,
            room_id=self.room_id,
            is_sender=True,
            created_at=_time_now,
            is_seen=True,
            uuid=str(uuid4()),
            msg_status='message_log',
            is_log_msg=True,
            log_message=UclLogDetail(
                log_type=log_type,
                message=log_msg,
                room_id=self.room_id,
                from_user=self.client_id,
                to_user=self.fchat_id,
                created_at=_time_now
            ),
            type=constants.CHAT_TYPE_FCHAT,
            chat_type=constants.CHAT_TYPE_FCHAT
        )
