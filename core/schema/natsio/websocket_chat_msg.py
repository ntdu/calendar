# -*- coding: utf-8 -*-
from typing import Any, List

from core.abstractions import CustomBaseModel


class WebsocketChatMessage(CustomBaseModel):
    """This is data format for messages which sent from CoreChat to Websocket Client
        - from CoreChat Worker to Webhook Service
        - from CoreChat Worker to ChatWS Service

    Args:
        to_clients (List[string]): list of user id
        sio_event (str): is an instance of string, value must matching with FE socketio client
        data (Any): wrapped data
    """
    to_clients: List[str]       # user ids
    sio_event: str              # socketio event name
    data: Any                   # bytes or string or any
