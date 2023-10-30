# -*- coding: utf-8 -*-
import os

# import kombu
from celery import Celery, bootsteps  # noqa: F401
from kombu import Exchange, Queue

from .service_settings import service_settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", service_settings.DJANGO_SETTINGS_IMPORT)

app = Celery("noti_service")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.task_queues = (
    Queue('hello1', Exchange('noti1.exchange'), routing_key='hello1'),
)
app.conf.task_default_queue = 'hello1'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'hello1'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()




















# connection = kombu.Connection(
#     hostname=service_settings.CELERY_BROKER_RABBITMQ_HOST,
#     port=service_settings.CELERY_BROKER_RABBITMQ_PORT,
#     username=service_settings.CELERY_BROKER_RABBITMQ_USERNAME,
#     password=service_settings.CELERY_BROKER_RABBITMQ_PASSWORD,
#     connect_timeout=5,
#     heartbeat=1
# )

# # with app.pool.acquire(block=True) as conn:
# with connection as conn:
#     exchange = kombu.Exchange(
#         name="noti.exchange",
#         type='direct',
#         durable=True,
#         channel=conn,
#     )
#     exchange.declare()
#     noti_queue = kombu.Queue(
#         name="noti.queue",
#         exchange=exchange,
#         routing_key="noti.routing",
#         channel=conn,
#         message_ttl=600,
#         queue_arguments={
#             'x-queue-type': 'classic'
#         },
#         durable=True
#     )
#     qnoti_name = noti_queue.declare()


# # setting consumer
# class NotiConsumerStep(bootsteps.ConsumerStep):
#     def get_consumers(self, channel):
#         from src.consumer.noti_consumer import noti_callback_handler
#         return [
#             kombu.Consumer(
#                 channel,
#                 queues=[noti_queue],
#                 callbacks=[noti_callback_handler],
#                 accept=['json'],
#                 no_ack=True
#             )
#         ]


# conn = app.pool.acquire(block=True)
# try:
#     app.steps['consumer'].add(NotiConsumerStep)
#     connection.ensure_connection(max_retries=3)
#     print(" **************************************************************** ")
# except connection.connection_errors:
#     print(" +++++++++++++++++++++++++++++++++++++++++++++++++ ")
#     connection.ensure_connection(max_retries=3)
