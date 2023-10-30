# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from core import constants
from kombu import Connection, Exchange, Producer
from kombu.pools import connections as connection_pool
from kombu.pools import producers as producer_pool

from .base import BaseClient


class RabbitMqClient(BaseClient):
    def _singleton_init(self, **kwargs) -> Any:
        self.is_connected: bool = False
        self.exchanges: Dict[str, Exchange] = {}
        self.connections: Dict[str, Connection] = {}
        self.connection_pool = connection_pool
        self.producer_pool = producer_pool
        return super()._singleton_init(**kwargs)

    def get_default_connection(self, connection_name) -> Connection:
        connection = self.connections.get(connection_name, None)
        if connection and isinstance(connection, Connection):
            return connection

        for connection_url, connection_instance in self.connections.items():
            return connection_instance

    def get_exchange(self, exchange_name: str, exchange_type: str = 'direct'):
        if exchange_name in self.exchanges:
            return self.exchanges[exchange_name]
        self.exchanges[exchange_name] = Exchange(
            exchange_name,
        )
        return self.exchanges[exchange_name]

    def connect(self, amqp_urls: List[str]) -> None:
        if self.is_connected:
            return

        connection = Connection(amqp_urls, failover_strategy='round-robin')
        self.connections[amqp_urls] = connection
        self.connection_pool[connection]
        self.logger.info(f'Connected to RabbitMQ {self.connections=} | {self.connection_pool=}')

    def _publish(
        self,
        data: Any,
        exchange: str,
        routing_key: str,
        cnt_name: str = None,
        exchange_type: str = 'direct',
        **kwargs,
    ):
        connection = self.get_default_connection(cnt_name)
        if isinstance(exchange, str):
            exchange = self.get_exchange(exchange)
        if not isinstance(exchange, Exchange):
            self.logger.error(f'Exchange {exchange} is not instance of Exchange')
            return
        with self.producer_pool[connection].acquire(block=True) as producer:
            producer: Producer
            return producer.publish(
                data,
                exchange=exchange,
                routing_key=routing_key,
                declare=[exchange],
                serializer='json',
                # compression='zlib', # Not using compression in NOC # NOSONAR
                retry=True,
                retry_policy={
                    'interval_start': 0,  # First retry immediately,
                    'interval_step': 2,  # then increase by 2s for every retry.
                    'interval_max': 30,  # but don't exceed 30s between retries.
                    'max_retries': 10,   # give up after 30 tries.
                },
            )

    def publish_test(self, data: Dict[str, Any] = {'test': 'test'}):
        result = self._publish(
            data={'test': 'test'},
            exchange=constants.RABBITMQ_LOCALTEST_EXCHANGE,
            routing_key=constants.RABBITMQ_LOCALTEST_ROUTING_KEY,
        )
        self.log_publish_result(
            result, data,
            exchange_name=constants.RABBITMQ_LOCALTEST_EXCHANGE,
            routing_key=constants.RABBITMQ_LOCALTEST_ROUTING_KEY,
        )
