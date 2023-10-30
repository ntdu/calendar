# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, Tuple

from redis.asyncio import Redis


class AbsClient(ABC):
    @property 
    @abstractmethod
    def client(self) -> Redis:
        """Master client if use sentinel

        Raises:
            NotImplementedError: _description_

        Returns:
            Redis: _description_
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def slave_client(self) -> Redis:
        """Slave client if use sentinel else just redis client

        Raises:
            NotImplementedError: _description_

        Returns:
            Redis: _description_
        """
        raise NotImplementedError


class AbsRedisMixin(AbsClient):
    @abstractmethod
    async def publish(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def subscribe(self, *args, **kwargs):
        raise NotImplementedError


class AbsRedisClient(AbsRedisMixin, AbsClient):
    @abstractmethod
    async def connect(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self, *args, **kwargs):
        raise NotImplementedError


class AbsRedisManager(ABC):
    @abstractmethod
    def add_cache_client(self, name: str, client: AbsRedisClient, connect_params: Tuple = tuple(), klass: Any = None):
        raise NotImplementedError

    @abstractmethod
    def get_cache_client(self, name: str | int) -> AbsRedisClient:
        raise NotImplementedError

    @abstractmethod
    def remove_cache_client(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def add_pubsub_client(self, name: str, client: AbsRedisClient, connect_params: Tuple = tuple(), klass: Any = None):
        raise NotImplementedError

    @abstractmethod
    def get_pubsub_client(self, name: str | int) -> AbsRedisClient:
        raise NotImplementedError

    @abstractmethod
    def remove_pubsub_client(self, name: str):
        raise NotImplementedError

    @abstractmethod
    async def publish_all_clients(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def subscribe_all_clients(self, *args, **kwargs):
        raise NotImplementedError
