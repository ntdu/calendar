# -*- coding: utf-8 -*-

from typing import Dict, Optional

from core import constants
from core.abstractions import CustomBaseModel


class BaseNatsPubSubMessage(CustomBaseModel):
    route_type: Optional[str] = None
    manager_type: Optional[str] = None
    chat_type: Optional[str] = None  # for finding chat manager get from typeChat for fit old version
    msg_type: Optional[str] = None  # for finding core router get from typeMessage for fit old version

    @property
    def nats_headers(self) -> Dict:
        headers = {}
        for attr in (
            'route_type',
            'manager_type',
            'chat_type',
            'msg_type',
        ):
            if hasattr(self, attr) and getattr(self, attr):
                headers[attr] = getattr(self, attr)
        # print('nats header ', headers)
        return headers

    def set_old_version(self):
        self.senderId = getattr(self, 'sender_id', None)
        self.recipientId = getattr(self, 'recipient_id', None)
        self.appId = getattr(self, 'app_id', None)
        self.typeChat = getattr(self, 'chat_type', None)

    #   Facebook
    #
    def set_is_facebook_chat_message(self):
        # facebook chat message to webhook then to corechat
        self.route_type = constants.ROUTE_TYPE_CHAT
        self.manager_type = constants.MANAGER_TYPE_WEBHOOK_CHAT_MESSAGE
        self.chat_type = constants.CHAT_TYPE_FACEBOOK
        self.msg_type = constants.MSG_TYPE_TEXT

    #   ZALO
    #

    def set_is_zalo_chat_message(self):
        # zalo chat message
        self.route_type = constants.ROUTE_TYPE_CHAT
        self.manager_type = constants.MANAGER_TYPE_WEBHOOK_CHAT_MESSAGE
        self.chat_type = constants.CHAT_TYPE_ZALO
        self.msg_type = constants.MSG_TYPE_TEXT

    def set_is_zalo_actions_event(self, message_type: str):
        # zalo chat message
        self.route_type = constants.ROUTE_TYPE_CHAT
        self.manager_type = constants.MANAGER_TYPE_CHAT_ACTIONS
        self.chat_type = constants.CHAT_TYPE_ZALO
        self.msg_type = message_type

    #   FCHAT
    #

    def set_is_fchat_message(self):
        self.route_type = constants.ROUTE_TYPE_CHAT
        self.manager_type = constants.MANAGER_TYPE_WEBHOOK_CHAT_MESSAGE
        self.chat_type = constants.CHAT_TYPE_FCHAT
        self.msg_type = constants.MSG_TYPE_TEXT

    def set_is_fchat_user_chat_log(self):
        self.route_type = constants.ROUTE_TYPE_CHAT
        self.manager_type = constants.MANAGER_TYPE_USER_CHAT_LOG
        self.chat_type = constants.CHAT_TYPE_FCHAT
        self.msg_type = constants.MSG_TYPE_CHAT_LOG
