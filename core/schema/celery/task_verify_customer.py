# -*- coding: utf-8 -*-

from typing import Optional

from core.abstractions import CustomBaseModel


class CeleryTaskVerifyCustomerModel(CustomBaseModel):
    name: Optional[str] = ""
    email: Optional[str] = ""
    facebook_id: Optional[str] = ""
    phone: Optional[str] = ""
    zalo_id: Optional[str] = ""
    type: Optional[str] = ""
    avatar: Optional[str] = ""
    fanpage: Optional[str] = ""
    fanpage_url: Optional[str] = ""
    approach_date: Optional[str] = ""
    room_id: Optional[str] = ""
    x_auth_user_id: Optional[str] = ""
    noc_auth_user: Optional[str] = ""
