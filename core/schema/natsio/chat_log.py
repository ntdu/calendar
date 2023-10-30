# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from core import constants
from core.abstractions import CustomBaseModel
from django.utils import timezone

from .base_pubsub import BaseNatsPubSubMessage
from .chat_msg_to_ws_client import ChatMessageToWsClient, CmwLogMessageDetail


class UclLogDetail(CustomBaseModel):
    log_type: Optional[str] = None
    message: Optional[str] = None
    room_id: Optional[str] = None
    from_user: Optional[str] = None
    to_user: Optional[str] = None
    created_at: Optional[str] = None

    def convert_to_CmwLogMessageDetail(self, mid: str):
        return CmwLogMessageDetail(
            mid=mid,
            log_type=self.log_type,
            message=self.message,
            room_id=self.room_id,
            from_user=self.from_user,
            to_user=self.to_user,
            created_at=self.created_at
        )


class UserChatLog(BaseNatsPubSubMessage):
    text: Optional[str] = None
    created_time: Optional[str] = None
    sender_id: Optional[str] = None
    senderId: Optional[str]     # should remove when migrations done
    recipient_id: Optional[str] = None
    recipientId: Optional[str]   # should remove when migrations done
    appId: Optional[str]       # should remove when migrations done
    typeChat: Optional[str]    # should remove when migrations done
    typeMessage: Optional[str] = 'text'      # should remove when migrations done
    room_id: Optional[str]
    is_sender: bool = True
    created_at: str
    is_seen: Optional[str] = None
    mid: Optional[str] = None
    uuid: Optional[str] = None
    msg_status: Optional[str] = None
    type: Optional[str] = None
    is_log_msg: Optional[bool] = True
    log_message: Optional[UclLogDetail] = None

    route_type: Optional[str] = constants.ROUTE_TYPE_CHAT
    manager_type: Optional[str] = constants.MANAGER_TYPE_USER_CHAT_LOG
    chat_type: Optional[str] = None  # for finding chat manager get from typeChat for fit old version
    msg_type: Optional[str] = constants.MSG_TYPE_CHAT_LOG

    def convert_to_ChatMessageToWsClient(self, **kwargs) -> ChatMessageToWsClient:
        return ChatMessageToWsClient(
            created_at=self.created_time,
            is_seen=self.is_seen,
            is_sender=self.is_sender,
            sender_id=self.sender_id,
            text=self.text,
            uuid=self.uuid,
            mid=self.mid,
            room_id=self.room_id,
            timestamp=self.convert_timestamp(),
            log_message=self.log_message.convert_to_CmwLogMessageDetail(self.mid) if self.log_message else None
        )

    def convert_create_time(self) -> datetime:
        for i in (
            '%Y-%m-%dT%H:%M:%S.%f',
        ):
            try:
                return datetime.strptime(self.created_time, i)
            except Exception:
                pass
        return timezone.now()

    def convert_timestamp(self) -> int:
        if self.created_time:
            return self.convert_create_time().timestamp()
