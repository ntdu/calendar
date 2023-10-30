# -*- coding: utf-8 -*-
from typing import List, Optional

from core.abstractions import CustomBaseModel

from ..natsio import WcmAttachment, WebhookChatMessage


class Sender(CustomBaseModel):
    id: str


class Recipient(CustomBaseModel):
    id: str


class PayloadAttachment(CustomBaseModel):
    url: Optional[str]
    sticker_id: Optional[str]


class Attachment(CustomBaseModel):
    type: str
    payload: PayloadAttachment


class Message(CustomBaseModel):
    mid: str
    text: Optional[str]
    attachments: List[Attachment] = []


class Read(CustomBaseModel):
    watermark: int


class Messaging(CustomBaseModel):
    sender: Sender
    recipient: Recipient
    timestamp: int
    message: Optional[Message]
    read: Optional[Read]

# End messinging----------------------------------------


class ValueFrom(CustomBaseModel):
    id: str
    name: str


class ChangeValue(CustomBaseModel):
    from_: Optional[ValueFrom]
    link: Optional[str]
    post_id: Optional[str]
    created_time: Optional[int]
    item: str
    photo_id: Optional[str]
    published: Optional[int]
    verb: str


class Change(CustomBaseModel):
    value: ChangeValue
    field: str

# End change -------------------------------------------


class MessageEntry(CustomBaseModel):
    id: str
    time: int
    messaging: List[Messaging] = []
    changes: List[Change] = []


class FacebookWebhookEventMessage(CustomBaseModel):
    object: str
    entry: List[MessageEntry]

    def show_info(self) -> str:
        return f'event {self.object=}'

    def convert_to_WebhookChatMessage(self) -> List[WebhookChatMessage]:
        results = []
        for entry in self.entry:
            for messaging in entry.messaging:
                if messaging.message and messaging.recipient and messaging.recipient.id:
                    _res = WebhookChatMessage(
                        sender_id=messaging.sender.id,
                        recipient_id=messaging.recipient.id,
                        timestamp=messaging.timestamp,
                        text=messaging.message.text,
                        mid=messaging.message.mid,
                        app_id=entry.id,
                        attachments=[
                            WcmAttachment(
                                type=attachment.type,
                                payloadUrl=attachment.payload.url
                            ) for attachment in messaging.message.attachments
                        ],
                    )
                    results.append(_res)
        return results
