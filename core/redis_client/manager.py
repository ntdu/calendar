# -*- coding: utf-8 -*-
import asyncio
import logging
import time
from typing import Any, Callable, Dict, Tuple

import redis
import ujson
from core import constants
from core.abstractions import AbsRedisClient, AbsRedisManager, SingletonClass
from pydantic import BaseModel


class PubSubTask(BaseModel):
    task: Any
    pattern: str
    handler: Callable

    def get_info(self):
        # for logging,
        # return only serializable data
        return {
            'task': f'{self.task}',
            'pattern': self.pattern,
            'handler': f'{self.handler}'
        }


class RedisConfigParams(BaseModel):
    params: Tuple 
    klass: Any

    def get_info(self):
        # for logging,
        # return only serializable data
        return {
            'params': f'{self.params}',
            'class': f'{self.klass}'
        }

class RedisManager(SingletonClass, AbsRedisManager):
    """Class Redis help to store connected client in dict
    redis_manager = RedisManager()
    single_client = RedisClient()
    await single_client.connect(...)

    sentinel = RedisSentinelClient()
    await sentinel.connect()

    redis_manager.add_cache_client(name, single_client)
    redis_manager.add_pubsub_client(name, sentinel)

    Args:
        SingletonClass (_type_): _description_
    """

    def _singleton_init(self, **kwargs):
        self.logger = kwargs.get('logger') or logging.getLogger(constants.CONSOLE_LOGGER)
        self._cache_clients: Dict[str, AbsRedisClient] = {}
        self._cache_client_configs: Dict[str, RedisConfigParams] = {}
        self._pubsub_clients: Dict[str, AbsRedisClient] = {}
        self._pubsub_client_configs: Dict[str, RedisConfigParams] = {}
        self._pubsub_tasks: Dict[str, PubSubTask] = {}

    def add_cache_client(self, name: str, client: AbsRedisClient, connect_params: Tuple = tuple(), klass: Any = None):
        if not isinstance(client, AbsRedisClient):
            raise ValueError(f'expected client is an instance of AbsRedisClient get {type(client)=}')
        self._cache_clients.update({name: client})
        if connect_params and klass:
            self._cache_client_configs.update({
                name: RedisConfigParams(
                    params=connect_params,
                    klass=klass
                )
            })

    def get_cache_client(self, name: str | int = constants.DEFAULT_CACHE_CLIENT_NAME) -> AbsRedisClient:
        return self._cache_clients.get(name)

    def remove_cache_client(self, name: str):
        if name in self._cache_clients:
            del self._cache_clients[name]

    def add_pubsub_client(self, name: str, client: AbsRedisClient, connect_params: Tuple = tuple(), klass: Any = None):
        if not isinstance(client, AbsRedisClient):
            raise ValueError(f'expected client is an instance of AbsRedisClient get {type(client)=}')
        self._pubsub_clients.update({name: client})
        if connect_params:
            self._pubsub_client_configs.update({
                name: RedisConfigParams(
                    params=connect_params,
                    klass=klass
                )
            })

    def add_pubsub_task(self, name: str, task: asyncio.Task, ps_pattern: str, handler: Callable):
        current_task = self._pubsub_tasks.get(name)
        if current_task:
            if not current_task.task.done() and not current_task.task.cancelled():
                self.logger.warning(
                    f'current task still alive {name}',
                    extra={
                        'running_task': current_task.get_info(),
                        'new_task': {
                            'task': f'{task}',
                            'pattern': ps_pattern,
                            'handler': f'{handler}'
                        }
                    }
                )
                return False
        self._pubsub_tasks.update({
            name: PubSubTask(
                task=task,
                pattern=ps_pattern,
                handler=handler
            )
        })
        self.logger.info(
            f'created pubsub task {name}',
            extra={
                'new_task': self._pubsub_tasks.get(name).get_info(),
                'task done': f'{task.done()}',
                'task cancelled': f'{task.cancelled()}'
            }
        )
        return True

    def get_pubsub_client(self, name: str | int = constants.DEFAULT_PUBUB_CLIENT_NAME) -> AbsRedisClient:
        return self._pubsub_clients.get(name)

    def remove_pubsub_client(self, name: str):
        if name in self._pubsub_clients:
            del self._pubsub_clients[name]

    async def publish_all_clients(self, *args, **kwargs):
        for name, client in self._pubsub_clients.items():
            await client.publish(*args, **kwargs)

    async def subscribe_all_clients(self, *args, **kwargs):
        for name, client in self._pubsub_clients.items():
            await client.subscribe(*args, **kwargs)

    async def create_and_add_pubsub_task(
        self,
        name: str,
        pattern: str,
        handler: Callable,
        redis_client: AbsRedisClient
    ):
        """This function is a shortcut to create new pubsub listener of redis
        then put data to socketio server handler to publish all socketio clients

        Args:
            name (str): name of task (asyncio)
            pattern (str): pattern for redis client listen on
            handler (Callable): process data get from redis pubsub
            redis_client (AbsRedisClient): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
        """
        if not isinstance(redis_client, AbsRedisClient):
            redis_client = self._pubsub_clients.get(constants.DEFAULT_PUBUB_CLIENT_NAME)
        task: asyncio.Task = await redis_client.psubscribe(
            pattern,
            handler
        )
        task.set_name(name)
        self.add_pubsub_task(task.get_name(), task, pattern, handler)

    async def _recreate_redis_pubsub_client(self, name: str):
        client_config = self._pubsub_client_configs.get(name)
        if client_config:
            redis_client = client_config.klass()
            try:
                await redis_client.connect(*client_config.params)
                self.add_pubsub_client(name, redis_client, client_config.params, client_config.klass)
                self.logger.info('re-create redis pubsub client success')
            except Exception as e:
                self.logger.exception(
                    f're-create redis pubsub client get exception {e}',
                    extra=client_config.get_info()
                )

    async def tracking_redis_pubsub_connections(self, **kwargs):
        while True:
            await asyncio.sleep(kwargs.get('interval', 60))
            for name, redis_client in self._pubsub_clients.items():
                if redis_client:
                    try:
                        await redis_client.client.ping()
                    except redis.exceptions.ConnectionError:
                        # get data recreate new redis client
                        await self._recreate_redis_pubsub_client(name)
                    except Exception as e:
                        self.logger.exception(f'tracking_redis_pubsub_connections get exception {e}')

    async def tracking_redis_pubsub_tasks(self, **kwargs):
        while True:
            await asyncio.sleep(kwargs.get('interval', 30))
            for name, pubsub_task in self._pubsub_tasks.items():
                if pubsub_task.task.done() or pubsub_task.task.cancelled():
                    self.logger.info(f'found finished task or cancelled task {name}')
                    try:
                        await self.create_and_add_pubsub_task(
                            name,
                            pubsub_task.pattern,
                            pubsub_task.handler,
                            self._pubsub_clients.get(constants.DEFAULT_PUBUB_CLIENT_NAME)
                        )
                    except Exception as e:
                        self.logger.exception(
                            f'run process create_and_add_pubsub_task get exception {e}',
                            extra={
                                'ps_pattern': pubsub_task.pattern,
                                'handler': f'{pubsub_task.handler}'
                            }
                        )

    async def allow_to_ping(self, interval: float) -> bool:
        int_interval = int(interval)
        redis_client = self._pubsub_clients.get(constants.DEFAULT_PUBUB_CLIENT_NAME)
        if not redis_client:
            return False
        try:
            key = f'ws_service_allow_ping_{int(time.time() // int_interval * int_interval)}'
            pipe = redis_client.client.pipeline()
            pipe.incr(key)
            pipe.expire(key, 2 * int_interval)
            count, _ = await pipe.execute()
            print(f'count {count=} {_=}')
            if count == 1:
                return True
            return False
        except Exception as e:
            self.logger.exception(f'run allow_to_ping get exception {e}, return True')
            return True

    async def ping_keep_redis_connections(self, **kwargs):
        while True:
            await asyncio.sleep(kwargs.get('interval', 60))
            if not await self.allow_to_ping(kwargs.get('interval', 60)):
                continue
            redis_client = self._pubsub_clients.get(constants.DEFAULT_PUBUB_CLIENT_NAME)
            for name, pubsub_task in self._pubsub_tasks.items():
                if pubsub_task and pubsub_task.pattern:
                    try:
                        await redis_client.client.publish(
                            pubsub_task.pattern,
                            ujson.dumps({'ping': 'keep alive connection'})
                        )
                        self.logger.info(f'ping keep redis connection {name=}')
                    except Exception as e:
                        self.logger.exception(f'ping keep redis connection get exception {e}')
