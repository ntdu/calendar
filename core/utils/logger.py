# -*- coding: utf-8 -*-
import collections
import logging
import os
import sys
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
from typing import Dict, List

from core import constants
from django.http import HttpRequest
from pythonjsonlogger import jsonlogger
from rest_framework.request import Request

LOG_FORMAT = "%(asctime)s [process %(process)-6.8s] [%(levelname)-5.5s]: %(message)s"
LOG_FORMAT_WITH_NAME = "%(asctime)s [process %(process)-4.8s] [%(levelname)-4.4s] [%(name)-5.15s]: %(message)s"
JSON_FORMAT = '%(asctime)s %(levelname)s %(funcName)s %(pathname)s %(message)s %(exc_info)s'


default_formatter = logging.Formatter(LOG_FORMAT_WITH_NAME)


class CustomJsonFormatter(jsonlogger.JsonFormatter):

    def __init__(self, *args, **kwargs):
        if 'rename_fields' in kwargs:
            kwargs['rename_fields'].update({"asctime": "time", "levelname": "level"})
        else:
            kwargs['rename_fields'] = {"asctime": "time", "levelname": "level"}
        super().__init__(*args, **kwargs)
        self.datefmt = '[%d/%b/%Y:%H:%M:%S +0000]'

    def format(self, record):
        return super().format(record)

    def _parse_server_message(self, message: str):
        if not message:
            return ""
        parsed_msg = message.split(' ')
        return {
            'method': parsed_msg[0],
            'url_path': parsed_msg[1],
            'component': constants.LOG_COMPONENT_API,
        }

    def _handle_django_server_record(self, record: collections.OrderedDict):
        record['message'] = record.get('message', "").replace('"', '')
        try:
            parsed_msg = self._parse_server_message(record['message'])
            if isinstance(parsed_msg, dict):
                record.update(parsed_msg)
        except Exception:
            pass

        for remove_key in ('name', 'request', 'server_time'):
            if remove_key in record:
                del record[remove_key]

    def _handle_django_request_record(self, record: collections.OrderedDict):
        ...

    def _handle_sop_console_record(self, record: collections.OrderedDict):
        for remove_key in ('name', 'request', 'server_time'):
            if remove_key in record:
                del record[remove_key]

    def _handle_record_for_specific_name(self, record: collections.OrderedDict):
        record_name = record.get('name')
        if record_name == 'django.server':
            self._handle_django_server_record(record)
        if record_name == 'django.request':
            self._handle_django_request_record(record)
        if record_name == constants.CONSOLE_LOGGER:
            self._handle_sop_console_record(record)

    def process_log_record(self, record: collections.OrderedDict):
        self._handle_record_for_specific_name(record)

        # move time to first
        if 'level' in record:
            record.move_to_end('level', last=False)
        if 'time' in record:
            record.move_to_end('time', last=False)

        return super().process_log_record(record)


json_formatter = CustomJsonFormatter(
    fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
    rename_fields={"asctime": "time", "levelname": "level"},  # <--- added this line
    # datefmt="%Y-%m-%dT%H:%M:%S.%fZ",
    # json_indent=4
)


def set_logger_json_formatter(logger_names: List[str], only_console: bool = False):
    for name in logger_names:
        logger = logging.getLogger(name)
        # print('logger', name, logger, logger.handlers)
        for handler in logger.handlers:
            if only_console:
                if isinstance(handler, logging.StreamHandler):
                    handler.setFormatter(json_formatter)
                    # print('name', name, 'handler', handler, handler.formatter)
            else:
                handler.setFormatter(json_formatter)


def setup_logger(
    logger_name: str,
    level: int = logging.INFO,
    to_console: bool = True,
    to_file: bool = False,
    file_path: str = None,
    clear_existed_handlers: bool = False
) -> logging.Logger:
    """
    Create logger which write output to console and log file.
    Logging levels: https://docs.python.org/3/library/logging.html#logging-levels
    Format options: https://docs.python.org/3/library/logging.html#logrecord-attributes

    Args:
        logger_name (str): Name to identify logger and used as log file's name.
        level (int, optional): Level of log message will be included. Defaults to logging.INFO.
        to_console (bool, optional): send log to console
        to_file (bool, optional): allow to write log to file
        file_path (str, optional): file destination to save log, must enable by set to_file = True

    Returns:
        Logger: Logger class for manipulate message
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = False

    if clear_existed_handlers:
        logger.handlers = []

    if to_console:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(json_formatter)
        console_handler.setLevel(level)
        logger.addHandler(console_handler)

    # Time routate handler
    if to_file:
        if not os.path.isdir(file_path):
            raise ValueError(f'expected file_path is the os path, get -> {file_path}')

        time_rotate_handler = TimedRotatingFileHandler(file_path, when='midnight', interval=1, backupCount=100)
        time_rotate_handler.setFormatter(logging.Formatter(LOG_FORMAT_WITH_NAME))
        time_rotate_handler.setLevel(level)
        logger.addHandler(time_rotate_handler)

    return logger


def add_console_handler(logger_name: str):
    logger = logging.getLogger(logger_name)
    found_console_handler = False
    for hander in logger.handlers:
        if isinstance(hander, logging.StreamHandler):
            if hander.stream == sys.stdout:
                found_console_handler = True
                break
    if found_console_handler:
        return

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(json_formatter)
    console_handler.setLevel(logger.level)
    logger.addHandler(console_handler)
    return True



def restruct_logger(logger: logging.Logger):
    def restruct_log_method(func, exc_info: bool=None):
        @wraps(func)
        def structured_method(
            message,
            exc_info: bool = exc_info,
            extra: Dict = None,
            stack_info=False,
            stacklevel=1,
            **kwargs
        ):
            if not extra:
                extra = {}

            # django request
            for k, v in kwargs.items():
                if k == 'request' and isinstance(v, (Request, HttpRequest)):
                    # get request infomation automatically
                    request_headers = v.headers
                    request_url_path = v.get_full_path()
                    extra.update({
                        'url_path': request_url_path,
                        'method': v.method,
                        'component': constants.LOG_COMPONENT_API,
                        'headers': str({
                            keyheader: valueheader
                            for keyheader, valueheader in request_headers.items() if (
                                k.lower().startswith('x-')
                                or k.lower().startswith('auth')
                            )
                        })
                    })

            # extra.update(kwargs)

            # load default extra by code
            if kwargs.get('log_code'):
                log_extra_by_code = constants.LOG_CODES.get(kwargs.get('log_code'))
                if log_extra_by_code and isinstance(log_extra_by_code, dict):
                    extra.update(log_extra_by_code)
        
            for k, v in kwargs.items():
                if k in constants.ALLOW_CUSTOM_EXTRA_FROM_KWARGS:
                    extra[k] = v

            return func(
                message,
                exc_info=exc_info,
                extra=extra,
                stack_info=stack_info,
                stacklevel=stacklevel,
            )
        return structured_method

    logger.debug = restruct_log_method(logger.debug)
    logger.info = restruct_log_method(logger.info)
    logger.warn = restruct_log_method(logger.warn)
    logger.error = restruct_log_method(logger.error)
    logger.critical = restruct_log_method(logger.critical)
    logger.exception = restruct_log_method(logger.exception, True)

    return logger
