# -*- coding: utf-8 -*-
from typing import List, Optional

from core import constants
from core.abstractions import CustomBaseModel

from ..natsio import WcmAttachment, WcmChatOptional, WebhookChatMessage


class LocationCoordinates(CustomBaseModel):
    latitude: str
    longitude: str


class AttachmentPayload(CustomBaseModel):
    id: Optional[str]
    coordinates: Optional[LocationCoordinates]
    thumbnail: Optional[str]
    url: Optional[str]
    description: Optional[str]
    size: Optional[str]
    name: Optional[str]
    checksum: Optional[str]
    type: Optional[str]


class MessageAttachment(CustomBaseModel):
    payload: Optional[AttachmentPayload]
    type: str


class Message(CustomBaseModel):
    msg_id: Optional[str]
    msg_ids: List[str] = []
    text: Optional[str]
    attachments: List[MessageAttachment] = []
    react_icon: Optional[str]
    conversation_id: Optional[str]


class Recipient(CustomBaseModel):
    id: str


class Sender(CustomBaseModel):
    id: str


class Follower(CustomBaseModel):
    id: str


class Customer(CustomBaseModel):
    id: str


class Info(CustomBaseModel):
    address: str
    phone: str
    city: str
    district: str
    name: str
    ward: str


class ZaloWebhookEventMessage(CustomBaseModel):
    app_id: str
    oa_id: Optional[str]
    user_id_by_app: Optional[str]
    event_name: str
    timestamp: str
    message: Optional[Message]
    sender: Optional[Sender]
    recipient: Optional[Recipient]
    user_id: Optional[str]
    source: Optional[str]
    follower: Optional[Follower]
    info: Optional[Info]
    customer: Optional[Customer]
    request_type: Optional[str]
    create_time: Optional[str]
    expired_time: Optional[str]
    confirmed_time: Optional[str]
    status_code: Optional[str]

    def show_info(self) -> str:
        return f'app {self.app_id} event {self.event_name} at {self.timestamp}'

    def find_page_id(self) -> str | None:
        if self.event_name in (
            constants.ZALO_EVENT_FOLLOW,
            constants.ZALO_EVENT_UNFOLLOW,
        ):
            page_id = self.oa_id
        else:
            if self.recipient:
                page_id = self.recipient.id
        return page_id

    def find_msg_type(self) -> str:
        if (
            self.follower
            and self.follower.id
            and self.event_name in (
                constants.ZALO_EVENT_FOLLOW,
                constants.ZALO_EVENT_UNFOLLOW
            )
        ):
            return constants.MSG_TYPE_CHAT_ACTION
        return constants.MSG_TYPE_TEXT

    @property
    def is_user_action_event(self) -> bool:
        return self.event_name in (
            constants.ZALO_EVENT_FOLLOW,
            constants.ZALO_EVENT_UNFOLLOW,
            constants.ZALO_EVENT_OA_SEND_TEXT,
        )

    @property
    def is_oa_send_text_event(self) -> bool:
        return self.event_name in (
            constants.ZALO_EVENT_OA_SEND_TEXT
        )

    @property
    def is_follow_unfollow_event(self) -> bool:
        return self.event_name in (
            constants.ZALO_EVENT_FOLLOW,
            constants.ZALO_EVENT_UNFOLLOW,
        )

    def create_follow_unfollow_chat_optional(self) -> WcmChatOptional:
        return WcmChatOptional(
            chat_type=constants.CHAT_TYPE_ZALO,
            data={
                'follower_id': self.sender.id if self.sender else None,
                'follow': True if self.event_name == constants.NATS_MSG_TYPE_FOLLOW else False
            }
        )

    def convert_to_WebhookChatMessage(self) -> WebhookChatMessage:
        nats_attachments = []
        if self.message and self.message.attachments:
            for attachment in self.message.attachments:
                if attachment.payload:
                    nats_attachments.append(
                        WcmAttachment(
                            name=attachment.payload.name,
                            type=attachment.payload.type,
                            payloadUrl=attachment.payload.url,
                            size=attachment.payload.size,
                            att_type=attachment.type,
                            att_id=attachment.payload.id
                        )
                    )

        optionals = []
        # type follow/unfollow
        if self.is_follow_unfollow_event:
            self.sender = Sender(id=self.follower.id)
            self.recipient = Recipient(id=self.oa_id)
            optionals.append(self.create_follow_unfollow_chat_optional())

        return WebhookChatMessage(
            sender_id=self.sender.id,
            recipient_id=self.recipient.id if self.recipient else None,
            timestamp=int(self.timestamp),
            text=self.message.text if self.message else None,
            mid=self.message.msg_id if self.message else None,
            app_id=self.app_id,
            attachments=nats_attachments,
            optionals=optionals
        )
