# -*- coding: utf-8 -*-
import json
from typing import Any, Dict

from core import constants
from core.templates.settings import FacebookSetting
from pydantic import BaseModel

from .base import BaseApiConnector


class FacebookApiConnector(BaseApiConnector):
    def _initialize(self, setting: FacebookSetting, **kwargs):
        self.app_id = setting.FACEBOOK_APP_ID
        self.app_secret = setting.FACEBOOK_APP_SECRET
        self.api_domain = setting.FACEBOOK_GRAPH_API_DOMAIN
        self.api_version_domain = '/'.join([
            setting.FACEBOOK_GRAPH_API_DOMAIN,
            setting.FACEBOOK_GRAPH_API_VERSION
        ])

    def _create_send_file_body(
        self,
        recipient_id: str,
        content_type: str,
        **kwargs
    ) -> Dict:
        return {
            'tag': 'CUSTOMER_FEEDBACK',
            'messaging_type': 'MESSAGE_TAG',
            'recipient': '{"id":"recipient_id"}'.replace(
                'recipient_id', recipient_id
            ),
            'message': '{"attachment":{"type":"file_type","payload":{"is_reusable":true}}}'.replace(
                'file_type', content_type
            ),
        }

    def _create_send_text_body(self, recipient_id: str, text: str):
        return {
            "messaging_type": "MESSAGE_TAG",
            "recipient": {
                "id": recipient_id
            },
            "tag": "CUSTOMER_FEEDBACK",
            "message": {
                "text": text
            }
        }

    def get_chat_message_by_mid(self, access_token: str, message_id: str, return_json: bool = False):
        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/{message_id}/',
            params={
                'access_token': access_token,
                'fields': 'message,created_time,from,to,attachments'
            },
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=return_json
        )

    def send_chat_text_message(self, access_token: str, recipient_id: str = None, data: Any = None,):
        if isinstance(data, dict):
            data = json.dumps(data)
        elif isinstance(data, str):
            if not recipient_id:
                raise ValueError('if you specify data is a string, you must provide recipient_id')
            data = self._create_send_text_body(recipient_id, data)
        elif isinstance(data, BaseModel):
            data = data.json()
        else:
            raise ValueError('only accept data in an instance of (dict, str, pydantic.BaseModel)')

        return self._fetch(
            method='POST',
            url=f'{self.api_domain}/me/messages',
            params={'access_token': access_token},
            payload=data,
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False
        )

    def send_chat_file_message(
        self,
        access_token: str = None,
        data: Any = None,
        file: Any = None,
        **kwargs
    ):
        return self._fetch(
            method='POST',
            url=f'{self.api_domain}/me/messages',
            params={'access_token': access_token},
            payload=data['payload'],
            files=file,
            return_json=False,
            request_timeout=100
        )

    def get_user_info(self, access_token: str, user_id: str, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/{user_id}',
            params={
                'fields': "first_name,last_name,profile_pic,gender,name",
                'access_token': access_token
            },
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=True
        )

    def get_fanpage_info(self, access_token: str, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/me',
            params={'access_token': access_token},
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            **kwargs
        )

    def check_fanpage_token(self, access_token: str, page_id: str, return_json: bool = False, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/{page_id}/conversations',
            params={'access_token': access_token},
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=return_json,
        )

    def get_fanpage_account(self, access_token: str, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/me/accounts',
            params={'access_token': access_token},
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False
        )

    def get_follower_count(self, access_token: str, page_id: str, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/{page_id}',
            params={
                'fields': "followers_count,fan_count",
                'access_token': access_token
            },
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False
        )

    def get_fb_pic(self, access_token: str, page_id: str, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/{page_id}',
            params={
                'fields': 'picture,link',
                'access_token': access_token
            },
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False
        )

    def get_fanpage_access_token(self, redirect_url: str, code: str, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/oauth/access_token',
            params={
                'redirect_uri': redirect_url,
                'code': code,
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'scope': "email"
            },
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False
        )

    def unsubscribe_fanpage(self, access_token: str, page_id: str, **kwargs):
        return self._fetch(
            method='DELETE',
            url=f'{self.api_version_domain}/{page_id}/subscribed_apps',
            params={'access_token': access_token},
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False
        )

    def subscribe_fanpage(self, access_token: str, page_id: str, **kwargs):
        return self._fetch(
            method='POST',
            url=f'{self.api_version_domain}/{page_id}/subscribed_apps',
            payload={
                'access_token': access_token,
                'subscribed_fields': 'messages,messaging_postbacks,feed,inbox_labels,message_reads,message_reactions'
            },
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False
        )

    def get_fanpage_conversations(self, access_token: str, page_id: str, **kwargs):
        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/{page_id}/conversations',
            params={'access_token': access_token},
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False,
        )

    def get_rooms_of_fanpage(self, access_token: str, page_id: str, after: str, **kwargs):
        # US #1728 FB. Đồng bộ tin nhắn
        """Fetches a list of chat rooms for a Facebook fan page.

        Args:
            access_token (str): A string representing the Facebook access token for authentication.
            page_id (str): A string representing the Facebook fan page ID for which to fetch chat rooms.
            after (str): A string representing the cursor that points to the end of the page of data to retrieve.

        Keyword Args:
            **kwargs: Additional arguments to pass to the `_fetch` method.

        Returns:
            bytes: The response content from the Facebook Graph API. This is a binary format of the JSON data,
            since `return_json` is set to `False`
        """

        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/{page_id}/conversations',
            params={'access_token': access_token, 'after': after},
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False,
        )

    def get_messages_of_room(self, access_token: str, room_id: str, after: str, **kwargs):
        # US #1728 FB. Đồng bộ tin nhắn
        """ Fetches messages for a given room.
        Args:
            access_token (str): A string representing the Facebook access token for authentication.
            room_id (str): The ID of the room to fetch messages for.
            after (str): The cursor for pagination. It points to the end of the current page of data.

        Keyword Args:
            **kwargs: Additional arguments to pass to the `_fetch` method.

        Returns:
            bytes: The response content from the Facebook Graph API. This is a binary format of the JSON data,
            since `return_json` is set to `False`
        """
        fields = "id,created_time,from,to,message,attachments,sticker"

        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/{room_id}/messages',
            params={'fields': fields, 'access_token': access_token, 'after': after},
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False,
        )

    def get_attachments_of_message(self, access_token: str, message_id: str, after: str, **kwargs):
        # US #1728 FB. Đồng bộ tin nhắn
        """ Fetches attachments of a message.
        Args:
            access_token (str): A string representing the Facebook access token for authentication.
            message_id (str): The ID of the message to fetch attachments for.
            after (str): The cursor for pagination. It points to the end of the current page of data.

        Keyword Args:
            **kwargs: Additional arguments to pass to the `_fetch` method.

        Returns:
            bytes: The response content from the Facebook Graph API. This is a binary format of the JSON data,
            since `return_json` is set to `False`
        """
        return self._fetch(
            method='GET',
            url=f'{self.api_version_domain}/{message_id}/attachments',
            params={'access_token': access_token, 'after': after},
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False,
        )

    def api_require_phone_number(self, access_token: str, recipient_id: str, title: str, **kwargs):

        return self._fetch(
            method='POST',
            url=f'{self.api_domain}/me/messages',
            params={'access_token': access_token},
            payload=json.dumps({
                "recipient": {
                    "id": recipient_id,
                },
                "messaging_type": "MESSAGE_TAG",
                "tag": "CUSTOMER_FEEDBACK",
                "message": {
                    "text": title,
                    "quick_replies": [
                        {
                            "content_type": "user_phone_number",
                        }
                    ]
                },
            }),
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False
        )

    def api_require_email(self, access_token: str, recipient_id: str, title: str, **kwargs):

        return self._fetch(
            method='POST',
            url=f'{self.api_domain}/me/messages',
            params={'access_token': access_token},
            payload=json.dumps({
                "recipient": {
                    "id": recipient_id,
                },
                "messaging_type": "MESSAGE_TAG",
                "tag": "CUSTOMER_FEEDBACK",
                "message": {
                    "text": title,
                    "quick_replies": [
                        {
                            "content_type": "user_email",
                        }
                    ]
                },
            }),
            headers={'Content-Type': constants.HTTP_HEADER_APP_JSON},
            return_json=False
        )
