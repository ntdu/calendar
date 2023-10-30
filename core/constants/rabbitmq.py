# -*- coding: utf-8 -*-
# Testing
RABBITMQ_LOCALTEST_EXCHANGE = "localtest.exchange"
RABBITMQ_LOCALTEST_QUEUE = "localtest.queue"
RABBITMQ_LOCALTEST_ROUTING_KEY = "localtest.routingkey"


# Webhook
RABBITMQ_WEBHOOK_EXCHANGE = "webhook.exchange"
RABBITMQ_WEBHOOK_QUEUE = "webhook.queue"
RABBITMQ_WEBHOOK_ROUTING_KEY_FACEBOOK = "webhook.routing.facebook"
RABBITMQ_WEBHOOK_ROUTING_KEY_FCHAT = "webhook.routing.fchat"
RABBITMQ_WEBHOOK_ROUTING_KEY_ZALO = "webhook.routing.zalo"
RABBITMQ_WEBHOOK_ROUTING_KEY_INFO = "webhook.routing.info"

# Customer service
RABBITMQ_CUSTOMER_EXCHANGE = "customer.exchange"
RABBITMQ_CUSTOMER_QUEUE = "customer.queue"
RABBITMQ_CUSTOMER_ROUTING_KEY_VERIFY = "customer.routing.verify"
RABBITMQ_CUSTOMER_ROUTING_KEY_ASSIGN = "customer.routing.assign"
RABBITMQ_WEBHOOK_TO_CUSTOMER_EXCHANGE = 'webhook.exchange'
RABBITMQ_WEBHOOK_TO_CUSTOMER_QUEUE = "webhook.queue.follow"
RABBITMQ_CUSTOMER_ROUTING_KEY_VERIFY_ZALO_FOLLOW = 'webhook.routing.follow'


# Notification service
RABBITMQ_NOTI_EXCHANGE = "noti.exchange"
RABBITMQ_NOTI_ROUTING_KEY = "noti.routing"

# Log message
RABBITMQ_WEBHOOK_QUEUE_ACTIVITY_LOG = "customer.queue.activity-log"
RABBITMQ_WEBHOOK_CUSTOMER_KEY_ACTIVITY_LOG = "customer.routing.activity-log"
