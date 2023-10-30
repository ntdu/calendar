# -*- coding: utf-8 -*-
from .base import BaseHandler


class BaseConsummer(BaseHandler):
    parser_class = None

    def parse_event(self, event, **kwargs):
        # default parse using pydantic BaseModel
        # override this method if you need
        if isinstance(event, str):
            return self.parser_class.parse_raw(event)
        else:
            return self.parser_class.parse_obj(event)

    def handle(self, event, **kwargs):
        if self.parser_class:
            event = self.parse_event(event, **kwargs)
            if not event:
                raise ValueError(f'Parse event with {self.parser_class} get None -> {event=}')

        return super().handle(event, **kwargs)

    def handle_message(self, event, **kwargs):
        raise NotImplementedError('you must implement handle_message method')

    def log_received_event(self, body, message, **kwargs):
        self.logger.info(
            f'{self.__class__.__name__}: get new message', 
            rabbit_consumer_data={'body': body},
            rabbit_consumer_message={'message': message},
            **kwargs
        )

    def log_exception(self, exc, body, message, **kwargs):
        self.logger.exception(
            f'{self.__class__.__name__}: get exception {exc}', 
            rabbit_consumer_data={'body': body},
            rabbit_consumer_message={'message': message},
            **kwargs
        )