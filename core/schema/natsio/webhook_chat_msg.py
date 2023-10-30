# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from core import constants
from core.abstractions import CustomBaseModel
from pydantic import validator

from ..report_schema import DataReportWorker
from .base_pubsub import BaseNatsPubSubMessage
from .chat_log import UclLogDetail, UserChatLog
from .chat_msg_to_ws_client import (
    ChatMessageToWsClient,
    CmwAttachment,
    CmwMessageServiceSurveyUserInfo,
)


class WcmAttachment(CustomBaseModel):
    name: Optional[str]
    type: Optional[str]             # zalo payload type
    payloadUrl: Optional[str]
    size: Optional[str]
    att_type: Optional[str]        # att_type
    att_id: Optional[str]

    def get_zalo_attachment_type(self) -> str:
        if self.att_type == 'file':
            if self.type in ('doc', 'docx',):
                return 'application/msword'
            if self.type:
                return f'application/{self.type}'
            return self.att_type
        return self.type if self.type else self.att_type


class WcmUserInfo(CustomBaseModel):
    title: Optional[str]
    value: Optional[str]


class WcmChatOptional(CustomBaseModel):
    chat_type: str
    data: Optional[Dict] = {}


class WcmLogMessageSchema(CustomBaseModel):
    log_type: Optional[str]
    message: Optional[str]
    room_id: Optional[str]
    from_user: Optional[str]
    to_user: Optional[str]
    created_at: Optional[str]


class WebhookChatMessage(BaseNatsPubSubMessage):
    """This is data format for messages which sent from Webhook Service to CoreChat Worker
        - facebook message from customer
        - zalo message from customer
        - livechat message from anynomouse customer

    Args:

    """
    sender_id: Optional[str]  # senderId
    senderId: Optional[str]     # should remove when migrations done
    recipient_id: Optional[str]  # recipientId
    recipientId: Optional[str]   # should remove when migrations done
    timestamp: Optional[float]
    text: Optional[str]
    mid: Optional[str]
    app_id: Optional[str]  # appId
    appId: Optional[str]       # should remove when migrations done
    typeChat: Optional[str]    # should remove when migrations done
    typeMessage: Optional[str] = 'text'      # should remove when migrations done
    error_message: Optional[int] = None
    attachments: List[WcmAttachment] = []
    user_info: List[WcmUserInfo] = []
    optionals: List[WcmChatOptional] = []
    uuid: Optional[str] = ""
    room_id: Optional[str] = None
    log_message: Optional[WcmLogMessageSchema] = None

    is_welcome_msg: Optional[bool] = False  # Fchat welcome msg
    browser_origin: Optional[str] = None    # browser_origin of Fchat

    is_new_room: Optional[bool] = False                         # Check new room for log message
    is_new_chat: Optional[bool] = False                         # Check new chat
    is_new_conversation: Optional[bool] = False                 # Check new conversation for report saleman
    is_new_complete_conversation: Optional[bool] = False        # Check new conversation complete for report saleman
    new_feedback: Optional[bool] = False                        # New msg feedback - ex: Msg Fb/Zl/Fchat -> sale
    count_message: Optional[int] = 0                            # Count msg off room_live chat

    @validator('uuid')
    def auto_uuid(cls, v):
        if isinstance(v, str) and len(v) >= 20:
            return v
        return str(uuid4())

    def get_message_time(self) -> datetime:
        msg_timestamp = self.timestamp
        if msg_timestamp:
            if msg_timestamp > 1075653429804:
                msg_timestamp = msg_timestamp / 1000
            return datetime.fromtimestamp(msg_timestamp)
        else:
            return datetime.utcnow()

    def convert_new_core(self, chat_type: str = None):
        self.route_type = constants.ROUTE_TYPE_CHAT
        self.manager_type = constants.MANAGER_TYPE_WEBHOOK_CHAT_MESSAGE
        self.msg_type = constants.MSG_TYPE_TEXT
        self.chat_type = chat_type

    def set_core(self):
        self.route_type = constants.ROUTE_TYPE_CHAT
        self.manager_type = constants.MANAGER_TYPE_WEBHOOK_CHAT_MESSAGE

    def set_for_report_admin_salesman(self):
        self.is_new_room = True
        self.is_new_chat = True
        self.is_new_conversation = True
        self.new_feedback = True

    def convert_to_ChatMessageToWsClient(
        self,
        room_id: str,       # room chat id, not postgresql id
        user_ids: List[str],
        **kwargs
    ) -> ChatMessageToWsClient:
        attachments = [
            CmwAttachment(
                url=attachment.payloadUrl,
                type=attachment.type,
                name=attachment.name,
                size=attachment.size
            ) for attachment in self.attachments
        ]

        return ChatMessageToWsClient(
            attachments=attachments,
            created_at=self.get_message_time().isoformat(),
            is_seen=False,
            is_sender=False,
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
            user_id=user_ids if user_ids else [],
            timestamp=self.timestamp,
            event=constants.CUSTOMER_TO_SALEMAN
        )

    def convert_to_ChatMessageToWsClient_chatws_zalo(
        self,
        room_id: str,       # room chat id, not postgresql id
        user_ids: List[str],
        **kwargs
    ) -> ChatMessageToWsClient:
        attachments = [
            CmwAttachment(
                url=attachment.payloadUrl,
                type=attachment.get_zalo_attachment_type(),
                name=attachment.name,
                size=attachment.size
            ) for attachment in self.attachments
        ]
        # print(attachments)

        return ChatMessageToWsClient(
            attachments=attachments,
            created_at=self.get_message_time().isoformat(),
            is_seen=False,
            is_sender=False,
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
            user_id=user_ids if user_ids else [],
            timestamp=self.timestamp,
            event=constants.CUSTOMER_TO_SALEMAN
        )

    def convert_to_ChatMessageToWsClient_webhook_fchat(self) -> ChatMessageToWsClient:
        attachments = []
        user_info = []
        attachments = [
            CmwAttachment(
                url=attachment.payloadUrl,
                type=attachment.type,
                name=attachment.name,
                size=attachment.size
            ) for attachment in self.attachments
        ]
        is_sender = False
        if self.optionals:
            for item in self.optionals:
                if item.data.get("user_info"):
                    user_info = [
                        CmwMessageServiceSurveyUserInfo(
                            title=user_info['title'],
                            value=user_info['value']
                        )for user_info in item.data.get("user_info")
                    ]
                if item.data.get("is_sender"):
                    is_sender = item.data.get("is_sender")

        return ChatMessageToWsClient(
            attachments=attachments,
            service_survey=user_info,
            created_at=self.get_message_time().isoformat(),
            is_seen="",
            is_sender=is_sender,
            message_reply=None,
            reaction=None,
            recipient_id=self.recipient_id,
            reply_id=None,
            sender_id=self.sender_id,
            sender_name=None,
            text=self.text,
            uuid=self.uuid,
            mid=self.mid,
            room_id=self.room_id,
            user_id=[self.sender_id],
            event='Customer.To.SaleMan.ACK',
            timestamp=self.timestamp
        )

    def convert_to_ChatMessageToWsClient_chatws_fchat(
        self,
        room_id: str,
        to_users: List[str]
    ) -> ChatMessageToWsClient:
        attachments = []
        user_info = []
        attachments = [
            CmwAttachment(
                url=attachment.payloadUrl,
                type=attachment.type,
                name=attachment.name,
                size=attachment.size
            ) for attachment in self.attachments
        ]
        is_sender = False
        if self.optionals:
            for item in self.optionals:
                if item.data.get("user_info"):
                    user_info = [
                        CmwMessageServiceSurveyUserInfo(
                            title=user_info['title'],
                            value=user_info['value']
                        ) for user_info in item.data.get("user_info")
                    ]
                if item.data.get("is_sender"):
                    is_sender = item.data.get("is_sender")

        res = ChatMessageToWsClient(
            attachments=attachments,
            service_survey=user_info,
            created_at=self.get_message_time().isoformat(),
            is_seen="",
            is_sender=is_sender,
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
            event=constants.CUSTOMER_TO_SALEMAN,
            user_id=to_users if to_users else [],
            timestamp=self.timestamp
        )
        # print('data to websocket chat ws', res)
        return res

    def convert_to_report_admin_header(self, chat_type: str = None):
        self.route_type = constants.ROUTE_TYPE_REPORT
        self.manager_type = constants.MANAGER_TYPE_REPORT_ADMIN
        self.msg_type = constants.HANDLER_TYPE_REPORT_CHAT_REPORT_ADMIN
        self.chat_type = chat_type

    def convert_to_report_saleman_header(self, chat_type: str = None):
        self.route_type = constants.ROUTE_TYPE_REPORT
        self.manager_type = constants.MANAGER_TYPE_REPORT_SALEMAN
        self.msg_type = constants.HANDLER_TYPE_REPORT_CHAT_REPORT_SALEMAN
        self.chat_type = chat_type

    def convert_to_DataReportWorker(
        self,
        page_id: int = None,
        page_name: str = None,
        browser_origin: str = None,
        room_id: str = None,
        user_id: List = [],
        **kwargs
    ) -> DataReportWorker:
        data_report = DataReportWorker(
            page_id=page_id,
            page_name=page_name,
            browser_origin=browser_origin,
            room_id=room_id,
            report_timestamp=datetime.now().replace(minute=0, second=0, microsecond=0).timestamp(),
            uuid=self.uuid,
            type_chat=self.typeChat,
            user_id=user_id,
            is_new_chat=self.is_new_chat,
            is_new_conversation=self.is_new_conversation,
            is_new_complete_conversation=self.is_new_complete_conversation,
            type_event=constants.ROUTE_TYPE_REPORT,
            new_feedback=self.new_feedback
        )
        return data_report

    def convert_to_UserChatLog(
        self,
        log_type: str,
        log_msg: str,
        from_user: str = None,
        to_user: str = None,
        log_time: float = 0.0,
    ) -> UserChatLog:
        if log_time:
            _time_now = datetime.fromtimestamp(log_time).isoformat()
        else:
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
                from_user=from_user or self.sender_id,
                to_user=to_user or self.recipient_id,
                created_at=_time_now
            ),
            type=self.chat_type,
            chat_type=self.chat_type
        )
