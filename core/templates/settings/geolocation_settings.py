# -*- coding: utf-8 -*-
from typing import Optional

from .base_settings_mixin import BaseSettingMixin


class GeoLocationSetting(BaseSettingMixin):
    SERVICE_GEOLOCATION_SERVICE_DOMAIN: Optional[str] = "https://api.geoapify.com/v1/geocode/reverse"
    SERVICE_GEOLOCATION_API_KEY: Optional[str]

    SERVICE_GEOLOCATION_BY_IP_SERVICE_DOMAIN: Optional[str] = "https://api-bdc.net/data/ip-geolocation-full"
    SERVICE_GEOLOCATION_BY_IP_API_KEY: Optional[str]
