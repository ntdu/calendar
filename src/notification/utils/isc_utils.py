# -*- coding: utf-8 -*-
import logging

from core import constants
from core.connectors import FacebookApiConnector, ISCApiConnector

logger = logging.getLogger(constants.CONSOLE_LOGGER)
isc_connector = ISCApiConnector()
fb_connector = FacebookApiConnector()


def get_token(username, password):
    try:
        response = isc_connector.get_token(username=username, password=password)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print('Get exception in get_token', e)
        return None


def send_notification_to_isc(access_token: str, data: dict):
    try:
        response = isc_connector.send_message(access_token=access_token, data=data)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {'Code': 401}
        else:
            return None

    except Exception as e:
        print('Get exception in send_notification_to_isc', e)
        return None
