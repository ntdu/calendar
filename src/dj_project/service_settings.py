# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

try:
    import core  # noqa
except ModuleNotFoundError:
    current_path = Path(os.getcwd())
    sys.path.append(str(current_path.parents[1]))

from core.connectors import ISCApiConnector
from core.templates.settings import (
    AppServiceSetting,
    CelerySetting,
    DjangoSetting,
    FirebaseSetting,
    GunicornSetting,
    RedisSetting,
)

SELECTED_ENV_NAME = os.environ.get("APP_ENV_NAME")


class ChatServiceSettings(
    AppServiceSetting,
    RedisSetting,
    DjangoSetting,
    CelerySetting,
    GunicornSetting,
    FirebaseSetting
):
    DJANGO_SETTINGS_IMPORT = 'src.dj_project.settings'


# Even when using a dotenv file, pydantic will still read environment variables as well as the dotenv file,
# environment variables will always take priority over values loaded from a dotenv file.
__env_file_path = ChatServiceSettings.get_env_file_path(ChatServiceSettings.get_selected_env())
service_settings = ChatServiceSettings(_env_file=__env_file_path)
service_settings.setup(__env_file_path)