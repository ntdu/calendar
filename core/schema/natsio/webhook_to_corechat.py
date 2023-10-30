# -*- coding: utf-8 -*-
from typing import Dict, List, Optional

from core import constants
from core.abstractions import CustomBaseModel


class WebhookToCorechatChatMessageAttachment(CustomBaseModel):
    type: Optional[str]
    payloadUrl: Optional[str]
    name: Optional[str]
    size: Optional[int]


class WebhookToCorechatChatOptional(CustomBaseModel):
    chat_type: str
    data: Optional[Dict] = {}


class WebhookToCorechatChatMessage(CustomBaseModel):
    senderId: str
    recipientId: str
    timestamp: int
    text: Optional[str]
    mid: Optional[str]
    appId: str
    attachments: List[WebhookToCorechatChatMessageAttachment] = []
    typeChat: str
    typeMessage: Optional[str] = constants.NATS_MSG_TYPE_TEXT
    optionals: List[WebhookToCorechatChatOptional] = []
    room_id: Optional[str]

    def bytes(self) -> bytes:
        return self.json().encode()
