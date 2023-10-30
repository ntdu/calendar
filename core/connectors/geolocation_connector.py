# -*- coding: utf-8 -*-
from core.templates.settings import GeoLocationSetting

from .base import BaseApiConnector


class GeoLocationApiConnector(BaseApiConnector):
    def _initialize(self, setting: GeoLocationSetting, **kwargs):
        self.geolocation_service_domain = setting.SERVICE_GEOLOCATION_SERVICE_DOMAIN
        self.geolocation_api_key = setting.SERVICE_GEOLOCATION_API_KEY

        self.geolocation_from_ip_service_domain = setting.SERVICE_GEOLOCATION_BY_IP_SERVICE_DOMAIN
        self.geolocation_from_ip_api_key = setting.SERVICE_GEOLOCATION_BY_IP_API_KEY

    def get_location_from_lat_lng(self, lat: float, lng: float, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.geolocation_service_domain}',
            params={
                'lat': lat,
                'lon': lng,
                'apiKey': self.geolocation_api_key
            },
            return_json=False,
        )

    def get_location_from_ip(self, ip: str, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.geolocation_from_ip_service_domain}',
            params={
                'ip': ip,
                'key': self.geolocation_from_ip_api_key,
                'localityLanguage': 'en'
            },
            return_json=False,
        )
