# -*- coding: utf-8 -*-
from typing import Dict  # noqa: F401

from core import constants  # noqa: F401
from core.templates.settings import AppServiceSetting

from .base import BaseApiConnector


class LocalServiceConnector(BaseApiConnector):
    def _initialize(self, setting: AppServiceSetting, **kwargs):
        self.local_user_service_domain: str = setting.SERVICE_USER_SERVICE_DOMAIN
        self.local_customer_service_domain: str = setting.SERVICE_CUSTOMER_SERVICE_DOMAIN
        self.zalo_distribution_msg_list_salesman = self.local_user_service_domain + setting.SERVICE_USER_SERVICE_API_ZALO_SALESMAN  # noqa

    def get_zalo_distributed_salesmans(
        self,
        page_id: str = None,
        **kwargs
    ):
        return self._fetch(
            method='GET',
            url=self.zalo_distribution_msg_list_salesman,
            params={"pageId": page_id},
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=True
        )
