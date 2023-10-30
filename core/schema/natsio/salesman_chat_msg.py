# -*- coding: utf-8 -*-
import time
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from core import constants
from core.abstractions import CustomBaseModel
from core.schema.natsio import DataReportWorker
from django.utils import timezone
from pydantic import BaseModel

from .base_pubsub import BaseNatsPubSubMessage
from .chat_log import UclLogDetail, UserChatLog
from .chat_msg_to_ws_client import ChatMessageToWsClient, CmwAttachment, CmwErrorMessageModel


class CoreChatInputMessage(BaseModel):
    msg_type: str
    chat_type: str


class ScmSendMessageAttachment(CustomBaseModel):
    id: Optional[str]
    type: Optional[str]
    url: Optional[str]
    name: Optional[str]
    size: Optional[str]
    video_url: Optional[str]


class ScmLogMessageSchema(CustomBaseModel):
    log_type: Optional[str]
    message: Optional[str]
    room_id: Optional[str]
    from_user: Optional[str]
    to_user: Optional[str]
    created_at: Optional[str]


class UpdateRoom(CustomBaseModel):
    room_id: str
    status: Optional[str]
    event: Optional[str] = 're-open-room'
    user_id: str


class SalesmanChatMessage(BaseNatsPubSubMessage):
    """This is data format for messages which sent from Chat Service to CoreChat Worker
        - facebook message from salesman
        - zalo message from salesman
        - livechat message from salesman

    Args:

    """
    mid: Optional[str]
    attachments: List[ScmSendMessageAttachment] = []
    text: Optional[str] = None
    created_time: Optional[str]
    sender_id: Optional[str]
    recipient_id: Optional[str]
    error_message: Optional[int] = None
    room_id: Optional[str]
    is_sender: bool = True
    created_at: Optional[str]
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
    log_message: Optional[ScmLogMessageSchema] = None

    def convert_new_core(self):
        self.route_type = constants.ROUTE_TYPE_CHAT
        self.manager_type = constants.MANAGER_TYPE_SALESMAN_SEND_MESSAGE
        self.msg_type = self.msg_status
        self.chat_type = self.type

    def set_core(self):
        self.route_type = constants.ROUTE_TYPE_CHAT
        self.manager_type = constants.MANAGER_TYPE_SALESMAN_SEND_MESSAGE

    def convert_to_ChatMessageToWsClient(
        self,
        room_id: str,       # room chat id, not postgresql id
        user_ids: List[str],
        socketio_event: str,
        error_message: Dict = None,
        **kwargs
    ) -> ChatMessageToWsClient:
        attachments = [
            CmwAttachment(
                url=attachment.url if attachment.url else None,
                video_url=attachment.video_url if attachment.video_url else None,
                type=attachment.type,
                name=attachment.name,
                size=attachment.size,
            ) for attachment in self.attachments
        ]
        return ChatMessageToWsClient(
            attachments=attachments,
            created_at=timezone.now().isoformat(),
            is_seen=False,
            is_sender=True,
            message_reply=None,
            reaction=None,
            recipient_id=self.recipient_id,
            reply_id=None,
            sender_id=self.sender_id,
            sender_name=None,
            text=self.text,
            uuid=self.uuid,
            mid=self.mid,
            room_id=room_id,
            created_time=None,
            user_id=user_ids,
            timestamp=int(time.time()),
            error_message=CmwErrorMessageModel.parse_obj(error_message) if error_message else None,
            event=socketio_event
        )

    def convert_to_ChatMessageToWsClient_webhook_fchat(
        self,
        room_id: str,       # room chat id, not postgresql id
        error_message: Dict = None,
        **kwargs
    ) -> ChatMessageToWsClient:
        attachments = [
            CmwAttachment(
                url=attachment.url if
                attachment.url else None,
                type=attachment.type,
                name=attachment.name,
                size=attachment.size,
            ) for attachment in self.attachments
        ]
        return ChatMessageToWsClient(
            attachments=attachments,
            created_at=timezone.now().isoformat(),
            is_seen=False,
            is_sender=True,
            message_reply=None,
            reaction=None,
            recipient_id=self.recipient_id,
            reply_id=None,
            sender_id=self.sender_id,
            sender_name=None,
            text=self.text,
            uuid=self.uuid,
            mid=self.mid,
            room_id=room_id,
            created_time=None,
            user_id=[self.recipient_id] if self.recipient_id else [],
            timestamp=int(time.time()),
            error_message=CmwErrorMessageModel.parse_obj(error_message) if error_message else None,
            event='SaleMan.To.Customer'
        )

    def convert_to_ChatMessageToWsClient_chatws_fchat(
        self,
        room_id: str,       # room chat id, not postgresql id
        user_ids: List[str],
        error_message: Dict = None,
        **kwargs
    ) -> ChatMessageToWsClient:
        attachments = [
            CmwAttachment(
                url=attachment.url if
                attachment.url else None,
                type=attachment.type,
                name=attachment.name,
                size=attachment.size,
            ) for attachment in self.attachments
        ]
        return ChatMessageToWsClient(
            attachments=attachments,
            created_at=timezone.now().isoformat(),
            is_seen=False,
            is_sender=True,
            message_reply=None,
            reaction=None,
            recipient_id=None,
            reply_id=None,
            sender_id=self.sender_id,
            sender_name=None,
            text=self.text,
            uuid=self.uuid,
            mid=self.mid,
            room_id=room_id,
            created_time=None,
            user_id=user_ids,
            timestamp=int(time.time()),
            error_message=CmwErrorMessageModel.parse_obj(error_message) if error_message else None,
            event='SaleMan.To.Customer.ACK'
        )

    def convert_from_send_msg_to_DataReportWorker(
        self,
        page_id: int = None,
        room_id: str = None,
        chat_type: str = None,
        page_name: str = "",
        uuid: str = "",
        is_new_chat: bool = False,
        is_new_conversation: bool = False,
        is_new_complete_conversation: bool = False,
        msg_feedback: bool = False,
        time_feedback: int = 0,
        old_feedback_time: int = 0
    ):
        _data_report = DataReportWorker(
            page_id=page_id,
            page_name=page_name,
            room_id=room_id,
            report_timestamp=old_feedback_time,
            uuid=uuid,
            type_chat=chat_type if chat_type != constants.CHAT_TYPE_LIVECHAT else constants.CHAT_TYPE_FCHAT,
            user_id=[],
            is_new_chat=is_new_chat,
            is_new_conversation=is_new_conversation,
            is_new_complete_conversation=is_new_complete_conversation,
            new_feedback=False,
            msg_feedback=msg_feedback,
            time_feedback=time_feedback,
            old_feedback_time=old_feedback_time
        )
        return _data_report

    def convert_to_UserChatLog(self, log_type: str, log_msg: str) -> UserChatLog:
        _time_now = datetime.utcnow().isoformat()
        return UserChatLog(
            text=log_msg,
            created_time=_time_now,
            sender_id=self.sender_id,
            recipient_id=self.recipient_id,
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
                from_user=self.sender_id,
                to_user=self.recipient_id,
                created_at=_time_now
            ),
            type=self.chat_type,
            chat_type=self.chat_type
        )
