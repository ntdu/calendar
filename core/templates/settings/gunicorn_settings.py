# -*- coding: utf-8 -*-
from typing import Optional

from .base_settings_mixin import BaseSettingMixin


class GunicornSetting(BaseSettingMixin):
    GUNICORN_HOST: str = '0.0.0.0'
    GUNICORN_PORT: str = '5002'
    GUNICORN_BIND_PATH: Optional[str] = None
    GUNICORN_WORKER_CONCURRENCY: Optional[int] = 4

    GUNICORN_ACCESS_LOG: Optional[str] = '-'    # default log to console
    GUNICORN_ERROR_LOG: Optional[str] = '-'     # default log to console

    class Config:
        case_sensitive = True
        validate_assignment = True
