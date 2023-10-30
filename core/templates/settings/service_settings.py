# -*- coding: utf-8 -*-
import logging
import os
from datetime import timezone
from typing import Dict, List, Optional

from .base_settings_mixin import BaseSettingMixin


class AppServiceSetting(BaseSettingMixin):
    SERVICE_BASE_DIR: Optional[str] = os.getcwd()
    SERVICE_LOG_LEVEL: int = logging.INFO

    # Service time and timezone
    SERVICE_USE_TZ: Optional[bool] = False
    SERVICE_TIMEZONE: Optional[timezone] = timezone.utc

    # Service info
    SERVICE_HOST: Optional[str] = ""
    SERVICE_PORT: Optional[int] = 0
    SERVICE_DOMAIN: Optional[str] = "https://webhook.minhhv11.xyz"
    SERVICE_ENVIRONMENT_INFO: Optional[str] = ''

    # Project
    PROJECT_NAME: Optional[str] = 'Project Template'
    PROJECT_DESCRIPTION: str = 'Project Description'

    # Service proxy
    SERVICE_USE_PROXY: Optional[bool] = False
    SERVICE_PROXY_ADDR: Optional[str] = ""
    SERVICE_NO_PROXY: Optional[str] = ""

    # service info for heath check
    SERVICE_NAME: Optional[str] = "X Service"
    SERVICE_DESCRIPTION: Optional[str] = "X Service"
    SERVICE_PATH: Optional[str] = "x-service"
    SERVICE_ENABLE_API: bool = False
    SERVICE_API_MOUNT_PATH: Optional[str] = None
    SERVICE_SOCKETIO_ENABLE: bool = False
    SERVICE_SOCKETIO_MOUNT_PATH: Optional[str] = None
    SERVICE_SOCKETIO_EXTRA_MOUNT_PATH: Optional[str] = None
    SERVICE_PORT: Optional[int] = 3000
    SERVICE_CODE: Optional[str] = "python-fastapi"

    # other settings
    SERVICE_COPY_WEBHOOK_MSG_ENABLE: bool = False
    SERVICE_COPY_WEBHOOK_MSG_DOMAINS: List[str] = []
    SERVICE_COPY_WEBHOOK_FB_URL_PATH: Optional[str] = None

    # other services
    SERVICE_USER_SERVICE_DOMAIN: Optional[str] = "http://172.24.222.101:4002"
    SERVICE_USER_SERVICE_API_FILTER_USER_BY_NAME_URL: Optional[str] = '/api/user/valueOfFilters'
    SERVICE_USER_SERVICE_API_LIST_AGENT_URL: Optional[str] = '/api/user/list-agent'
    SERVICE_USER_SERVICE_API_FILTER_AGENT_URL: Optional[str] = '/api/user/list-user-ominichat'
    SERVICE_USER_SERVICE_API_USER_PROFILE_URL: Optional[str] = '/api/user/profile'
    SERVICE_USER_SERVICE_API_ZALO_SALESMAN: Optional[str] = '/api/social-config/config-info'
    SERVICE_CHAT_DOMAIN : Optional[str] = 'https://gateway-sop-dev.fpt.vn/chat-service'  # add chat_service url

    SERVICE_CUSTOMER_SERVICE_DOMAIN: Optional[str] = "http://172.24.222.101:4003"
    SERVICE_CUSTOMER_SERVICE_API_VERIFY_INFORMATION_URL: Optional[str] = '/api/customer/verify-information'
    SERVICE_CUSTOMER_SERVICE_API_UPDATE_INFORMATION_URL: Optional[str] = '/api/customer/omnichat'
    SERVICE_CUSTOMER_SERVICE_API_ASSIGN_CHAT_URL: Optional[str] = '/api/customer/assign-chat'
    SERVICE_CUSTOMER_SERVICE_API_ROOM_INFO: Optional[str] = '/api/customer/infor-room-id'
    SERVICE_CUSTOMER_SERVICE_API_GET_LIST_LABEL: Optional[str] = '/api/label/list'

    SERVICE_WEBHOOK_SERVICE_DOMAIN: Optional[str] = "https://webhook.minhhv11.xyz"

    # service CADS
    SERVICE_CADS_DOMAIN: Optional[str] = "https://cads-api.fpt.vn"
    SERVICE_CADS_API_CHAT_MESSAGE: Optional[str] = '/sop/chat'

    # Test for SOP service
    SERVICE_TEST = True
    ROOM_TEST = "abc1234567890"

    def get_service_info(self) -> Dict:
        return {
            "name": self.SERVICE_PATH,
            "port": self.SERVICE_PORT,
            "code": self.SERVICE_CODE
        }

    class Config:
        case_sensitive = True
        validate_assignment = True
