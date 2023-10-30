# -*- coding: utf-8 -*-
from typing import Dict, List, Optional

from core.abstractions import CustomBaseModel


class UserInfo(CustomBaseModel):
    id: Optional[str]
    external_id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    avatar: Optional[str]
    gender: Optional[str]


class FanPageInfo(CustomBaseModel):
    name: Optional[str]
    avatar_url: Optional[str]


class RoomInfo(CustomBaseModel):
    user_id: List[str] = []
    event: Optional[str] = 'New.RoomInfo'
    id: str
    room_id: Optional[str]
    name: str
    type: Optional[str] = None
    approved_date: str
    status: Optional[str] = None
    assign_reminder: Optional[Dict] = {}
    completed_date: Optional[str] = None
    conversation_id: Optional[str]
    created_at: str
    last_message: Optional[List[str]] = None
    unseen_message_count: Optional[int] = 0
    user_info: Optional[UserInfo] = None
    fanpage: Optional[FanPageInfo] = None
    label: List[str] = []
