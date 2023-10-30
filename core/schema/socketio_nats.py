# -*- coding: utf-8 -*-
from typing import Any, List

from core.abstractions import CustomBaseModel


class SocketNatsSubscriberModel(CustomBaseModel):
    to_clients: List[str]
    sio_event: str
    data: Any
