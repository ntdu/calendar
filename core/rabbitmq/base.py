# -*- coding: utf-8 -*-
import logging
from typing import Any

from core import constants
from core.abstractions import SingletonClass


class BaseClient(SingletonClass):
    def _singleton_init(self, **kwargs) -> Any:
        self.logger: logging.Logger = kwargs.get(
            "logger",
            logging.getLogger(constants.CONSOLE_LOGGER)
        )

    def log_publish_result(
        self,
        result,
        data: Any,
        exchange_name: str,
        routing_key: str,
        **kwargs
    ):
        self.logger.info(
            f'Published rabbitmq message, ready {result.ready}',
            exchange=exchange_name,
            routing_key=routing_key,
            rabbit_publish_data=data,
            rabbit_publish_result={
                "ready": result.ready,
                "failed": result.failed,
                "cancelled": result.cancelled,
            },
            ** kwargs,
        )
