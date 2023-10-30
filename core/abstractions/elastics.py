# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from elasticsearch import Elasticsearch


class AbsElasticsearchClient(ABC):
    @property
    @abstractmethod
    def client(self) -> Elasticsearch:
        """Master client if use sentinel

        Raises:
            NotImplementedError: _description_

        Returns:
            Redis: _description_
        """
        raise NotImplementedError

    @abstractmethod
    async def connect(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self, *args, **kwargs):
        raise NotImplementedError


class AbsElasticsearchManager(ABC):
    @abstractmethod
    def add_client(self, name: str, client: AbsElasticsearchClient):
        raise NotImplementedError

    @abstractmethod
    def get_client(self, name: str) -> AbsElasticsearchClient:
        raise NotImplementedError

    @abstractmethod
    def remove_client(self, name: str) -> None:
        raise NotImplementedError
