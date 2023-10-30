# -*- coding: utf-8 -*-
import logging
from .utils import setup_logger, restruct_logger
from .constants import (
    CONSOLE_LOGGER,
    DEBUG_LOGGER,
    DJANGO_SERVER_LOGGER
)


console_logger = setup_logger(CONSOLE_LOGGER)
console_logger = restruct_logger(console_logger)

debug_logger = setup_logger(DEBUG_LOGGER, level=logging.DEBUG)
debug_logger = restruct_logger(debug_logger)

redis_listener_logger = setup_logger(constants.REDIS_LISENER_CONSOLE_LOGGER)
redis_listener_logger = restruct_logger(redis_listener_logger)

console_logger.info('setup console-logger done')
debug_logger.debug('setup debug-logger done')
redis_listener_logger.debug('setup redis-listener-logger done')
