# -*- coding: utf-8 -*-
from typing import List

from core.abstractions import AbsElasticsearchClient
from elasticsearch import Elasticsearch


class ElasticsearchClient(AbsElasticsearchClient):
    def __init__(
        self,
        elastic_urls: List[str],
        elastic_user: str,
        elastic_password: str,
        logtash_index: str,
        kibana_url: str
    ) -> None:
        self._client: Elasticsearch = None
        self._elastic_urls = elastic_urls
        self._elastic_user = elastic_user
        self._elastic_password = elastic_password
        self._logtash_indexl = logtash_index
        self._kibana_url = kibana_url

    @property
    def client(self) -> Elasticsearch:
        return self._client

    async def connect(self):
        self._client = Elasticsearch(
            hosts=[self._elastic_urls],
            basic_auth=(self._elastic_user, self._elastic_password,)
        )

    async def disconnect(self, *args, **kwargs):
        return
