# -*- coding: utf-8 -*-
from typing import List, Optional

from core import constants
from core.abstractions import CustomBaseModel
from django.utils import timezone

from .natsio.base_pubsub import BaseNatsPubSubMessage


class DataReportByHour(CustomBaseModel):
    page_id: Optional[int | str] = None
    browser_origin: Optional[str] = None
    page_name: Optional[str] = ""
    type: str
    feedback_rate: int = 0
    feedback_time: float
    numbers_conversation: int = 0
    complete_conversation: int
    timestamp: int
    created_at: str
    numbers_new_feedback: int = 0
    numbers_msg_feedback: int = 0
    time_feedback: int = 0


class DataReportWorker(BaseNatsPubSubMessage):
    page_id: Optional[int | str] = None
    page_name: Optional[str] = None
    browser_origin: Optional[str] = None
    room_id: str
    report_timestamp: Optional[int]
    uuid: Optional[str]
    type_chat: Optional[str] = constants.CHAT_TYPE_FACEBOOK
    user_id: List[str] = []
    is_new_chat: Optional[bool] = False
    is_new_conversation: Optional[bool] = False
    is_new_complete_conversation: Optional[bool] = False
    type_event: Optional[str] = 'report-router'
    new_feedback: Optional[bool] = False                        # New msg feedback - ex: Msg Fb/Zl/Fchat -> sale
    msg_feedback: Optional[bool] = False                        # Message feedback - ex: Msg sale -> Fb/Zl/Fchat
    time_feedback: Optional[int] = 0
    old_feedback_time: Optional[int] = 0                        # time feedback msg old

    def convert_to_DataReportByHour(self) -> DataReportByHour:
        _data_report = DataReportByHour(
            page_id=self.page_id,
            browser_origin=self.browser_origin,
            page_name=self.page_name,
            type=self.type_chat if self.type_chat != constants.CHAT_TYPE_LIVECHAT else constants.CHAT_TYPE_FCHAT,
            feedback_rate=0,
            feedback_time=0,
            numbers_conversation=0 if not self.is_new_conversation else 1,
            complete_conversation=0 if not self.is_new_complete_conversation else 1,
            numbers_new_feedback=0 if not self.new_feedback else 1,
            numbers_msg_feedback=0 if not self.msg_feedback else 1,
            timestamp=self.report_timestamp,
            created_at=str(timezone.now()),
            time_feedback=self.time_feedback
        )
        return _data_report


class DataReportWS(CustomBaseModel):
    id: str
    name: str
    page_id: Optional[str] = None
    page_url: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = False
    is_deleted: Optional[bool] = False
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    last_subscribe: Optional[str] = None
    type: Optional[str] = constants.CHAT_TYPE_FACEBOOK
    conversation_count: Optional[int] = 0
    followers_count: Optional[int] = 0
    likes_count: Optional[int] = 0
    user_id: List[str] = []
    event: Optional[str] = 'New.ReportData'


class ReportConversation(CustomBaseModel):
    page_id: int
    page_name: str = ""
    type: int
    numbers_conversation: int = 0
    complete_conversation: int
    timestamp: int
    created_at: str


class ReportFeedbackConversation(CustomBaseModel):
    page_id: int
    page_name: str = ""
    type: int
    feedback_rate: int = 0
    feedback_time: float
    timestamp: int
    created_at: str
