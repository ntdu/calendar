# -*- coding: utf-8 -*-
from typing import Dict

from core import constants
from core.abstractions import AbsElasticsearchClient, AbsElasticsearchManager, SingletonClass


class ElasticsearchManager(AbsElasticsearchManager, SingletonClass):
    def _singleton_init(self, **kwargs):
        self._clients: Dict[str, AbsElasticsearchClient] = {}

    def add_client(self, name: str, client: AbsElasticsearchClient):
        if not isinstance(client, AbsElasticsearchClient):
            raise ValueError(f'expected client is an instance of AbsElasticsearchClient get {type(client)=}')
        self._clients.update({name: client})

    def get_client(self, name: str | int = constants.DEFAULT_ELASTICSEARCH_CLIENT_NAME) -> AbsElasticsearchClient:
        return self._clients.get(name)

    def remove_client(self, name: str):
        if name in self._clients:
            del self._clients[name]
