# -*- coding: utf-8 -*-

import logging
from typing import Any, Dict, List

import httpx
from core import constants
from core.abstractions import SingletonClass


class BaseApiConnector(SingletonClass):

    def _singleton_init(self, **kwargs):
        self.logger = kwargs.get('logger') or logging.getLogger(constants.CONSOLE_LOGGER)
        self._is_initialized: bool = False

    def _initialize(self, settings, **kwargs):
        raise NotImplementedError

    def initialize(self, settings, **kwargs):
        if self._is_initialized:
            return
        try:
            self._initialize(settings, **kwargs)
        except Exception as e:
            self.logger.exception(f'initialize get exception {e}')
            raise e

        self._is_initialized = True

    def make_fetcher_resp(
        self,
        method: str,
        url: str,
        headers: Dict = {},     # NOSONAR
        params: Dict = {},
        payload: Dict = {},
        files: Any = None,
        auto_headers: bool = True,
        **kwargs
    ):
        if auto_headers and 'Content-Type' not in headers:
            headers.update({
                'Content-Type': constants.HTTP_HEADER_APP_JSON
            })
        return method, url, headers, params, payload, files

    def _fetch(
        self,
        method: str,
        url: str,
        headers: Dict = {},
        params: Dict = {},
        payload: Any = None,
        files: Any = None,
        auth: Any = None,
        client_verify: bool = False,
        request_timeout: int = 180,
        return_json: bool = True,
        **kwargs
    ) -> Dict | List | None:
        # print('come here', method, url, headers, params, payload)
        if not method or not url:
            raise ValueError(f'missing {method=} or {url}')
        try:
            with httpx.Client(timeout=request_timeout, verify=client_verify) as client:
                res: httpx.Response
                if method == 'GET':
                    res = client.get(url, params=params, headers=headers)
                elif method == 'POST':
                    if kwargs.get('is_noti_service'):
                        res = client.post(url, params=params, json=payload, auth=auth, headers=headers, files=files)
                    else:
                        res = client.post(url, params=params, data=payload, headers=headers, files=files)
                elif method == 'DELETE':
                    res = client.delete(url, params=params, headers=headers)
                else:
                    raise ValueError(f'method {method} not support')

                if return_json:
                    if res.status_code in (200, 201,):
                        return res.json()
                    else:
                        self.logger.error(
                            f'{self.__class__.__class__} fetch failed -> {res=} | {res.text=}'
                        )
                else:
                    return res
        except Exception as e:
            self.logger.exception(f'get exception {e}')
            return
