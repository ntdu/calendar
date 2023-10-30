# -*- coding: utf-8 -*-
from core import constants
from core.templates.settings import AppServiceSetting

from .base import BaseApiConnector


class UserApiConnector(BaseApiConnector):
    def _initialize(self, setting: AppServiceSetting, **kwargs):
        self.service_user_domain = setting.SERVICE_USER_SERVICE_DOMAIN
        self.api_user_profile = setting.SERVICE_USER_SERVICE_API_USER_PROFILE_URL
        self.api_filter_by_name = setting.SERVICE_USER_SERVICE_API_FILTER_USER_BY_NAME_URL
        self.api_list_agent = setting.SERVICE_USER_SERVICE_API_LIST_AGENT_URL
        self.api_filter_list_agent = setting.SERVICE_USER_SERVICE_API_FILTER_AGENT_URL
        self.api_zalo_sale_man = setting.SERVICE_USER_SERVICE_API_ZALO_SALESMAN

        self.user_profile_url = f'{self.service_user_domain}/me/messages'

    def get_user_profile(self, email: str, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.service_user_domain}{self.api_user_profile}',
            params={'email': email},
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False
        )

    def get_user_profile_by_user_id(self, user_id: str, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.service_user_domain}{self.api_user_profile}/{user_id}',
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            **kwargs
        )

    def get_zalo_agents(self, admin_id: str, **kwargs):
        """Get zalo agents from user-service
            resp = {
                "status": "success",
                "message": "success",
                "data": [
                    {
                        "id": "05da106f-1ed4-11ee-b0b3-005056a3619d",
                        "name": "Dương Đức Nhân",
                        "email": "nhandd3@fpt.com",
                        "avatar": null
                    },
                    ...
                ]
            }

        Args:
            admin_id (str): admin user-id of fanpage

        Returns:
            _type_: _description_
        """
        return self._fetch(
            method='GET',
            url=f'{self.service_user_domain}{self.api_list_agent}',
            headers={'Content-Type': 'application/json', 'x-auth-user-id': admin_id},
            **kwargs
        )

    def get_zalo_agents(self, admin_id: str, **kwargs):
        """Get zalo agents from user-service
            resp = {
                "status": "success",
                "message": "success",
                "data": [
                    {
                        "id": "05da106f-1ed4-11ee-b0b3-005056a3619d",
                        "name": "Dương Đức Nhân",
                        "email": "nhandd3@fpt.com",
                        "avatar": null
                    },
                    ...
                ]
            }

        Args:
            admin_id (str): admin user-id of fanpage 

        Returns:
            _type_: _description_
        """
        return self._fetch(
            method='GET',
            url=f'{self.service_user_domain}{self.api_list_agent}',
            headers={'Content-Type': 'application/json', 'x-auth-user-id': admin_id},
            **kwargs
        )
