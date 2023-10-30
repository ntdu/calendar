# -*- coding: utf-8 -*-
from .base_settings_mixin import BaseSettingMixin


class DatabaseMongoSetting(BaseSettingMixin):
    DB_MONGO_HOST: str
    DB_MONGO_PORT: int = 27017
    DB_MONGO_USERNAME: str
    DB_MONGO_PASSWORD: str
    DB_MONGO_DB_NAME: str
