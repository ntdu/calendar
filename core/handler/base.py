# -*- coding: utf-8 -*-
import logging

from core import constants
from core.abstractions import AbsHandler, SingletonClass


class BaseHandler(AbsHandler, SingletonClass):
    logger: logging.Logger

    def _singleton_init(self, **kwargs):
        self.logger = kwargs.get(
            'logger',
            logging.getLogger(constants.CONSOLE_LOGGER)
        )

    def handle(self, *args, **kwargs):
        try:
            self.handle_message(*args, **kwargs)
        except Exception as e:
            self.logger.exception(f'{self.__class__.__name__} handle message get exception {e}')

    def handle_message(self, *args, **kwargs):
        raise NotImplementedError('you must implement handle_message method')


class ChatWebhookEventBaseHandler(BaseHandler):
    logger: logging.Logger
    parser_class = None
    allowed_events = []

    def is_event_allowed(self, event, **kwargs):
        # always allow
        # if you need validate event, override this method
        return True

    def parse_event(self, event, **kwargs):
        if isinstance(event, str):
            return self.parser_class.parse_raw(event)
        else:
            return self.parser_class.parse_obj(event)

    def handle(self, event, **kwargs):
        if not self.is_event_allowed(event, **kwargs):
            return

        if self.parser_class:
            event = self.parse_event(event, **kwargs)
            if not event:
                raise ValueError(f'Parse event with {self.parser_class} get None -> {event=}')

        return super().handle(event, **kwargs)

    def handle_message(self, event, **kwargs):
        raise NotImplementedError('you must implement handle_message method')
