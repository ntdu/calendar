# -*- coding: utf-8 -*-
import logging
from typing import List, Optional, Tuple

from core import constants
from core.abstractions import AbsRedisClient
from redis.asyncio import Redis, Sentinel

from .mixins import DefaultMixins


class RedisSentinelClient(DefaultMixins, AbsRedisClient):
    def __init__(self, **kwargs) -> None:
        self._sentinel_client: Sentinel = None
        self._sentinel_name: Optional[str] = None
        self._master_client: Redis = None
        self._slave_client: Redis = None
        self._is_connected: bool = False
        self.logger = kwargs.get('logger') or logging.getLogger(constants.CONSOLE_LOGGER)

    @property
    def is_connected(self):
        return self._is_connected

    @property
    def client(self) -> Redis:
        return self._master_client

    @property
    def slave_client(self) -> Redis:
        return self._slave_client

    async def get_clients(self):
        master = await self._sentinel_client.discover_master(self._sentinel_name)
        slaves = await self._sentinel_client.discover_slaves(self._sentinel_name)
        self._master_client = self._sentinel_client.master_for(self._sentinel_name)
        if not slaves:
            self._slave_client = self._master_client
        else:
            self._slave_client = self._sentinel_client.slave_for(self._sentinel_name)
        self.logger.info(f'redis clients master {master} | slaves {slaves}')

    async def connect(
        self,
        sentinel_servers: List[Tuple[str, int]],
        sentinel_name: str,
        redis_db: int = 0,
        redis_password: str = None,
        decode_responses: bool = True,     # response is bytes (default)
        **kwargs
    ):
        if isinstance(self._sentinel_client, Sentinel):
            return
        try:
            self._sentinel_client = Sentinel(
                sentinel_servers,
                db=redis_db,
                password=redis_password,
                decode_responses=decode_responses
            )
            self._sentinel_name = sentinel_name
            await self.get_clients()

            self._name = f'Sentinel-Client-{sentinel_servers}'
            self._is_connected = True
            self.logger.info(f'RedisSentinelClient {self._name} | connected {self._is_connected}')
        except Exception as e:
            self.logger.exception(f'connect redis {sentinel_servers=} get exception {e}')

    async def disconnect(self):
        return
