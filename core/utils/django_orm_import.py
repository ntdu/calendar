# -*- coding: utf-8 -*-
import logging
import os

import django
from core import constants
from django.apps import apps

logger = logging.getLogger(constants.CONSOLE_LOGGER)


def setup_django_orm(django_settings: str = 'project.settings'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings)
    django.setup()


def get_django_model(app_name: str, model_name: str):
    for app_conf in apps.get_app_configs():
        try:
            return app_conf.get_model(model_name)
            return app_conf.get_model(f'{app_name}.{model_name}')
        except LookupError:
            continue
        except Exception as e:
            logger.exception(f'Could not found model {app_name}.{model_name} -> get exception {e}')
            raise e
    logger.warn(f'Could not found model {app_name}.{model_name}')
