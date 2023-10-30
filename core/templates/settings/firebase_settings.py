# -*- coding: utf-8 -*-
from typing import Optional

from .base_settings_mixin import BaseSettingMixin


class FirebaseSetting(BaseSettingMixin):
    FCM_SERVER_KEY: str
    FCM_CREDENTIALS: Optional[dict] = {}
    TYPE: Optional[str] = 'service_account'
    PROJECT_ID: str
    PRIVATE_KEY_ID: str
    PRIVATE_KEY: str
    CLIENT_EMAIL: str
    CLIENT_ID: str
    AUTH_URI: Optional[str] = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI: Optional[str] = 'https://oauth2.googleapis.com/token'
    AUTH_PROVIDER_X509_CERT_URL: Optional[str] = 'https://www.googleapis.com/oauth2/v1/certs'
    CLIENT_X509_CERT_URL: Optional[str] = 'https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-qzqpq%40sopdev-86855.iam.gserviceaccount.com'    # noqa # NOSONAR
    UNIVERSE_DOMAIN: Optional[str] = 'googleapis.com'

    def get_fcm_credentials(self):
        return {
            "type": self.TYPE,
            "project_id": self.PROJECT_ID,
            "private_key_id": self.PROJECT_ID,
            "private_key": self.PRIVATE_KEY,
            "client_email": self.CLIENT_EMAIL,
            "client_id": self.CLIENT_ID,
            "auth_uri": self.AUTH_URI,
            "token_uri": self.TOKEN_URI,
            "auth_provider_x509_cert_url": self.AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": self.CLIENT_X509_CERT_URL,
            "universe_domain": self.UNIVERSE_DOMAIN
        }
