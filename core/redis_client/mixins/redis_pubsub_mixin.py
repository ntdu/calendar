# -*- coding: utf-8 -*-
import asyncio
import inspect
import logging
from typing import Callable, Dict
import redis
import ujson
from core.abstractions import AbsRedisMixin, CustomBaseModel
from redis.client import PubSub


class RedisPubSubMixin(AbsRedisMixin):
    logger: logging.Logger

    def get_subscriber(self) -> PubSub:
        return self.slave_client.pubsub()

    async def handle_pubsub_msg(
        self,
        subscriber: PubSub,
        handler: Callable,
        handler_kwargs: Dict = {},
        sleep_time: float = 0.1,
        ignore_subscribe_messages: bool = False
    ):
        # Message Received: {'type': 'pmessage', 'pattern': b'channel:*', 'channel': b'channel:1', 'data': b'Hello'}
        try:
            while True:
                data = await subscriber.get_message(ignore_subscribe_messages)
                if data:
                    message = data['data']
                    if message:
                        try:
                            await handler(ujson.loads(message), **handler_kwargs)
                            continue
                        except Exception as e:
                            self.logger.exception(f'redis {subscriber=} handle {message=} get exception {e}')
                            continue
                await asyncio.sleep(sleep_time)
        except redis.exceptions.ConnectionError as e :
            self.logger.exception(f'get exception {e}')
            return

    async def subscribe(
        self,
        channel: str,
        handler: Callable,
        handler_kwawrgs: Dict = {},
        sleep_time: float = 0.1
    ):
        """_summary_

        Args:
            channel (str): _description_
            handler (Callable): _description_
            handler_kwawrgs (Dict, optional): _description_. Defaults to {}.
            sleep_time (float, optional): _description_. Defaults to 0.1.

        Raises:
            ValueError: _description_
        """
        if not inspect.iscoroutinefunction(handler):
            raise ValueError('handler must be a coroutine')

        subscriber: PubSub = self.get_subscriber()
        await subscriber.subscribe(channel, ignore_subscribe_messages=True)
        task = asyncio.create_task(
            self.handle_pubsub_msg(subscriber, handler, handler_kwawrgs, sleep_time, True)
        )
        self.logger.info(f'RedisPubSubMixin subscribe {channel=} with {handler} -> {task=}')

    async def psubscribe(
        self,
        channel: str,
        handler: Callable,
        handler_kwawrgs: Dict = {},
        sleep_time: float = 0.1
    ):
        """_summary_

        Args:
            channel (str): _description_
            handler (Callable): _description_
            handler_kwawrgs (Dict, optional): _description_. Defaults to {}.
            sleep_time (float, optional): _description_. Defaults to 0.1.

        Raises:
            ValueError: _description_
        """
        if not inspect.iscoroutinefunction(handler):
            raise ValueError('handler must be a coroutine')

        subscriber: PubSub = self.get_subscriber()
        await subscriber.psubscribe(channel, ignore_subscribe_messages=True)
        task = asyncio.create_task(
            self.handle_pubsub_msg(subscriber, handler, handler_kwawrgs, sleep_time, True)
        )
        self.logger.info(f'RedisPubSubMixin subscribe {channel=} with {handler} -> {task=}')
        return task

    async def publish(self, channel: str, message: CustomBaseModel | Dict):
        """_summary_

        Args:
            channel (str): _description_
            message (str): _description_

        Raises:
            ValueError: _description_
        """
        if not channel or not isinstance(channel, str):
            raise ValueError('channel must be an instance of string')

        if isinstance(message, dict):
            dumpped_msg = ujson.dumps(message)
        elif isinstance(message, CustomBaseModel):
            dumpped_msg = message.json()
        else:
            raise ValueError('accept message is an instance of dict or core.abstractions.CustomBaseModel')

        return await self.client.publish(channel, dumpped_msg)
