# -*- coding: utf-8 -*-
from datetime import datetime

from core import constants
from core.templates.settings import AppServiceSetting
from django.db import models

from .base import BaseApiConnector


class CADSApiConnector(BaseApiConnector):
    def _initialize(self, setting: AppServiceSetting, **kwargs):
        self.env = setting.SERVICE_ENVIRONMENT_INFO
        self.cads_domain = setting.SERVICE_CADS_DOMAIN
        self.url_send_chat_message = setting.SERVICE_CADS_API_CHAT_MESSAGE

    def send_chat_message(
        self,
        room: models.Model,
        message: str = None,
        log_text: str = None,
        log_action: str = None,
        message_time: datetime = None,
        **kwargs
    ):
        """ Data example
        _data = {
            "user_id": room.user_id,
            "room_id": room.room_id,
            "customer_id": room.external_id,
            "channel": room.type,
            "fanpages": {
                "name": room.page_id.name if room.type != constants.CHAT_CONNECTOR_TYPE_FCHAT else None,
                "page_id": room.page_id.name if room.type != constants.CHAT_CONNECTOR_TYPE_FCHAT else None,
                "avatar_url": room.page_id.avatar_url if room.type != constants.CHAT_CONNECTOR_TYPE_FCHAT else None
            },
            "message": message,
            "log_message": {
                "log_text": log_text,
                "log_action": log_action
            },
            "time_message": time_message.isoformat(),
            "env": settings.SERVICE_ENVIRONMENT_INFO,
            "extra_field": kwargs
        }
        """
        if not message_time:
            message_time = datetime.utcnow()

        fanpages = {
            "name": None,
            "page_id": None,
            "avatar_url": None
        }
        if room.type != constants.CHAT_CONNECTOR_TYPE_FCHAT:
            fanpages = {
                "name": room.page_id.name,
                "page_id": room.page_id.page_id,
                "avatar_url": room.page_id.avatar_url
            }

        payload = {
            "user_id": room.user_id,
            "room_id": room.room_id,
            "customer_id": room.external_id,
            "channel": room.type,
            "fanpages": fanpages,
            "message": message,
            "log_message": {
                "log_text": log_text,
                "log_action": log_action
            },
            "time_message": message_time.isoformat(),
            "env": self.env,
            "extra_field": kwargs
        }

        return self._fetch(
            method='POST',
            url=f'{self.cads_domain}{self.url_send_chat_message}',
            payload=payload,
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            **kwargs
        )
