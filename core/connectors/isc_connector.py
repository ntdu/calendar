# -*- coding: utf-8 -*-
import httpx
from core import constants
from core.templates.settings import AppServiceSetting

from .base import BaseApiConnector


class ISCApiConnector(BaseApiConnector):
    def _initialize(self, setting: AppServiceSetting, **kwargs):
        self.service_isc_domain = setting.SERVICE_ISC_SERVICE_DOMAIN
        self.api_get_token = setting.SERVICE_ISC_SERVICE_API_GET_ACCESS_TOKEN
        self.api_send_message = setting.SERVICE_ISC_SERVICE_API_SEND_MESSAGE

    def get_token(self, username: str, password: str, **kwargs):
        return self._fetch(
            method='POST',
            url=f'{self.service_isc_domain}{self.api_get_token}',
            payload={'GrantType': 'client_credentials'},
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            auth=httpx.BasicAuth(username, password),
            return_json=False,
            is_noti_service=True
        )

    def send_message(self, access_token: str, data: dict, **kwargs):
        return self._fetch(
            method='POST',
            url=f'{self.service_isc_domain}{self.api_send_message}',
            payload=data,
            params={'GrantType': 'client_credentials'},
            headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False,
            is_noti_service=True
        )
