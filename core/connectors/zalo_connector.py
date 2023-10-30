# -*- coding: utf-8 -*-
import json

from core import constants
from core.templates.settings import ZaloSetting

from .base import BaseApiConnector


class ZaloApiConnector(BaseApiConnector):
    def _initialize(self, setting: ZaloSetting, **kwargs):
        self.app_id = setting.ZALO_APP_ID
        self.app_secret = setting.ZALO_APP_SECRET_KEY
        self.open_api_domain = setting.ZALO_OA_OPEN_API
        self.api_v3_zaloa = setting.ZALO_OA_OPEN_API_V3
        self.auth_api_domain = setting.ZALO_OA_OAUTH_API

        self.url_get_oa_token = f'{self.auth_api_domain}/access_token'
        self.url_get_oa_info = f'{self.open_api_domain}/getoa'
        self.url_get_oa_followers = f'{self.open_api_domain}/getfollowers'
        self.url_get_oa_message = f'{self.open_api_domain}/message'
        self.url_get_oa_conversation = f'{self.open_api_domain}/conversation'
        self.url_get_user_profile = f'{self.open_api_domain}/getprofile'
        self.url_send_message_text = f'{self.api_v3_zaloa}/message/cs'
        self.url_upload_file = f'{self.open_api_domain}/upload'
        self.url_get_message_quota = f'{self.open_api_domain}/quota/message'
        self.url_listrecent_chat = f'{self.open_api_domain}/listrecentchat'

    def get_oa_token(
        self,
        authorization_code: str = None,
        verifier_code: str = None,
        refresh_token: str = None,
        app_id: str = None,
        app_secret: str = None,
        **kwargs
    ):
        app_id = app_id or self.app_id
        app_secret = app_secret or self.app_secret
        if refresh_token:
            payload = {
                'app_id': app_id,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        else:
            payload = {
                'code': authorization_code,
                'app_id': app_id,
                'grant_type': 'authorization_code',
            }
            if verifier_code is not None:
                payload.update({'code_verifier': verifier_code})

        return self._fetch(
            method='POST',
            url=self.url_get_oa_token,
            payload=payload,
            headers={'Content-Type': 'application/x-www-form-urlencoded', 'secret_key': app_secret},
            return_json=False
        )

    def get_oa_info(self, access_token: str, **kwargs):
        return self._fetch(
            method='GET',
            url=self.url_get_oa_info,
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON, 'access_token': access_token},
            return_json=False
        )

    def get_oa_followers(
        self,
        access_token: str = None,
        offset: int = 0,
        count: int = 5,
        tag_name: str = None,
        **kwargs
    ):
        params = {"offset": offset, "count": count, }
        if tag_name:
            params.update({'tag_name': tag_name})

        return self._fetch(
            method='GET',
            url=self.url_get_oa_followers + "?data=" + str(params),
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON, 'access_token': access_token},
            params=params,
            return_json=False,
        )

    def get_oa_conversations(
        self,
        access_token: str = None,
        user_id: str = None,
        offset: int = 0,
        count: int = 1,
        return_json=False,
        **kwargs
    ):
        return self._fetch(
            method='GET',
            url=self.url_get_oa_conversation,
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON, 'access_token': access_token},
            params={
                'data': {
                    'user_id': user_id,
                    'offset': offset,
                    'count': count,
                }
            },
            return_json=return_json,
            **kwargs
        )

    def get_message_quota(self, access_token: str, message_id: str, **kwargs):
        if message_id:  # reply message quota
            data = {'message_id': message_id}
        else:   # active message quota
            data = None

        return self._fetch(
            method='POST',
            url=self.url_get_message_quota,
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON, 'access_token': access_token},
            payload=data
        )

    def get_user_profile(self, access_token: str, user_id: str, **kwargs):
        return self._fetch(
            method='GET',
            url=self.url_get_user_profile,
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON, 'access_token': access_token},
            params={"data": {"user_id": user_id}}
        )

    def get_oa_message(self, access_token: str, user_id: str, **kwargs):
        payload = {
            'recipient': {
                'user_id': user_id,
            },
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'request_user_info',
                        'elements': [{
                            'title': 'OA Chatbot (Testing)',
                            'subtitle': 'Đang yêu cầu thông tin từ bạn',
                            'image_url': 'https://developers.zalo.me/web/static/zalo.png'
                        }]
                    }
                }
            },
        }
        return self._fetch(
            method='POST',
            url=self.url_get_user_profile,
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON, 'access_token': access_token},
            payload=payload
        )

    def send_chat_text_message(
        self,
        msg_type: str = 'text',
        last_message_zalo_id: str = None,
        access_token: str = None,
        recipient_id: str = None,
        text: str = None,
        attachment_token: str = None,
        attachment_id: str = None,
        **kwargs
    ):
        message = {}
        if msg_type == 'text':
            message: dict = {
                'text': text
            }
        elif msg_type == 'file':
            message = {
                "attachment": {
                    "type": "file",
                    "payload": {
                        "token": attachment_token,
                    }
                }
            }
        elif msg_type in ('sticker', 'image'):
            message = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [{
                            "media_type": msg_type,
                            "attachment_id": attachment_id
                        }]
                    }
                }
            }
        return self._fetch(
            method='POST',
            url=self.url_send_message_text,
            headers={
                "Content-Type": constants.HTTP_HEADER_APP_JSON,
                "access_token": access_token,
            },
            payload=json.dumps({
                "recipient": {
                    "user_id": str(recipient_id),
                    # "message_id": last_message_zalo_id,
                },
                "message": message,
            }),
            return_json=False
        )

    def send_chat_file_message(self, access_token, attachment_type, attachment):
        # wait ThienNK5
        return self._fetch(
            method='POST',
            url=f'{self.url_upload_file}/{attachment_type}',
            headers={'access_token': access_token},
            files=[
                ('file', (attachment.name, attachment, attachment_type))
                # ('file', (attachment.name, attachment, attachment.content_type))
            ],
            return_json=False
        )

    def send_reaction_message(self, access_token: str, user_id: str, react_icon: str, react_message_id: str):
        """Fetches reations from the Facebook.

        Args:
            access_token (str): A string representing the Facebook access token for authentication.
            user_id (str): A string representing the user_id.
            react_icon (str): A string representing the react_icon.
            react_message_id (str): A string representing the react_message_id.

        Returns:
            bytes: The response content from the Facebook Graph API. This is a binary format of the JSON data,
            since `return_json` is set to `False`
        """
        return self._fetch(
            method='POST',
            url=self.url_send_message_text,
            headers={
                "Content-Type": constants.HTTP_HEADER_APP_JSON,
                "access_token": access_token,
            },
            payload=json.dumps({
                "recipient": {
                    "user_id": user_id,
                },
                "sender_action": {
                    "react_icon": react_icon,
                    "react_message_id": react_message_id
                }
            }),
            return_json=False
        )

    def send_request_share_information(self, access_token: str, recipient_id: str, title: str, subtitle: str, image_url: str):
        """Fetches request share information zaloOA.

        Args:
            access_token (str): A string representing the Facebook access token for authentication.
            user_id (str): A string representing the user_id.
            title (str): A string representing the title.
            subtitle (str): A string representing the subtitle.

        Returns:
            bytes: The response content from the Facebook Graph API. This is a binary format of the JSON data,
            since `return_json` is set to `False`
        """
        message = {
            "attachment": {
                "type": "template",
                "payload": {
                        "template_type": "request_user_info",
                        "elements": [{
                            "title": title,
                            "subtitle": subtitle,
                            "image_url": image_url
                        }]
                }
            }
        }
        return self._fetch(
            method='POST',
            url=self.url_send_message_text,
            headers={
                "Content-Type": constants.HTTP_HEADER_APP_JSON,
                "access_token": access_token,
            },
            payload=json.dumps({
                "recipient": {
                    "user_id": str(recipient_id),
                },
                "message": message,
            }),
            return_json=False
        )

    def listrecent_chat(
        self,
        access_token: str = None,
        offset: int = 0,
        count: int = 10,
        **kwargs
    ):
        """Fetches reations from the Zalo.

        Args:
            access_token (str): A string representing the Zalo access token for authentication.

        Returns:
            bytes: The response content from the Zalo Graph API. This is a binary format of the JSON data,
            since `return_json` is set to `False`
        """
        params = {"offset": offset, "count": count}

        return self._fetch(
            method='GET',
            url=self.url_listrecent_chat + "?data=" + str(params),
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON, 'access_token': access_token},
            params=params,
            return_json=False,
        )
