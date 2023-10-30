# -*- coding: utf-8 -*-
from src.dj_project.service_settings import service_settings  # noqa     # isort:skip
from core.templates.gunicorn import create_gunicorn_config

gconfig = create_gunicorn_config(service_settings)

locals().update(gconfig)
