# -*- coding: utf-8 -*-
import logging
from functools import wraps
from typing import Callable, List

from core import constants
from kombu import Connection, Consumer, Exchange, Queue
from kombu.mixins import ConsumerMixin


def with_ack(function):
    @wraps(function)
    def wrapper(body, message):
        try:
            function(body, message)
            message.ack()
        except Exception as e:
            print(e)
            message.requeue()
    return wrapper


class BaseWorker(ConsumerMixin):
    def __init__(self, **kwargs):
        self.consummers: List[Consumer] = []
        self.connection = None
        self.logger: logging.Logger = kwargs.get(
            'logger',
            logging.getLogger(constants.CONSOLE_LOGGER)
        )

    def connect(self, rabbitmq_urls: str) -> None:
        self.connection = Connection(rabbitmq_urls, failover_strategy='round-robin')
        self.connection.ensure_connection(max_retries=3)
        self.logger.info(f'Connected to RabbitMQ {self.connection=}')

    def set_connection(self, connection: Connection):
        if isinstance(connection, Connection):
            self.connection = connection

    def add_consummer(self, queues: List[Queue], callbacks: List[Callable]):
        self.logger.info(f'Add consummer {queues=} {callbacks=}')
        self.consummers.append({
            'queues': queues,
            'callbacks': [with_ack(cb) for cb in callbacks]
        })

    def create_queue(
        self,
        exchange_name: str,
        exchange_type: str,
        queue_name: str,
        routing_key: str,
        **kwargs
    ) -> Queue:
        if exchange_type not in ('direct', 'topic', 'fanout'):
            raise ValueError('exchange_type must be direct, topic or fanout')
        with self.connection as conn:
            exchange = Exchange(exchange_name, type=exchange_type, durable=True, channel=conn)
            exchange.declare()

            queue = Queue(queue_name, exchange, routing_key=routing_key, channel=conn, durable=True, **kwargs)
            queue.declare()

        return queue

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=cinfo.get('queues'),
                accept=['pickle', 'json'],
                callbacks=cinfo.get('callbacks')
            ) for cinfo in self.consummers
        ]

    #
    #   Test block
    #
    def run_test(self, _tokens=1, **kwargs):
        try:
            self.setup_test()
            return super().run(_tokens, **kwargs)
        except KeyboardInterrupt:
            self.logger.info('bye bye')

    def setup_test(self):
        queue = self.create_queue(
            exchange_name=constants.RABBITMQ_LOCALTEST_EXCHANGE,
            exchange_type='direct',
            queue_name=constants.RABBITMQ_LOCALTEST_QUEUE,
            routing_key=constants.RABBITMQ_LOCALTEST_ROUTING_KEY,
            message_ttl=600,
            queue_arguments={
                'x-queue-type': 'classic'
            }
        )

        def test_handler(body, message):
            print(body)
        self.add_consummer([queue], [test_handler])
