# -*- coding: utf-8 -*-
import logging  # noqa

from core import constants

from .settings import ElasticseaerchSetting, RedisSetting

logger = logging.getLogger(constants.CONSOLE_LOGGER)


async def setup_redis(settings: RedisSetting):
    logger.info('startup-event: setup redis running...')
    from core.redis_client import RedisClient, RedisManager, RedisSentinelClient
    if settings.REDIS_SENTINEL_SERVERS:
        RedisClass = RedisSentinelClient        # noqa  # NOSONAR
        connect_params = (
            settings.REDIS_SENTINEL_SERVERS,
            settings.REDIS_SENTINEL_NAME,
            settings.REDIS_SENTINEL_REDIS_DB,
            settings.REDIS_SENTINEL_REDIS_PASSWORD,
        )
    else:
        RedisClass = RedisClient
        connect_params = (settings.get_redis_server_url(),)

    redis_manager = RedisManager()

    # for cache
    redis_cache = RedisClass()
    await redis_cache.connect(*connect_params)
    redis_manager.add_cache_client(
        constants.DEFAULT_CACHE_CLIENT_NAME,
        redis_cache
    )
    logger.info('startup-event: setup redis done')


async def setup_redis_with_sync_client(settings: RedisSetting):
    logger.info('startup-event: setup redis running...')
    from core.redis_client import RedisClient, RedisManager, RedisSentinelClient, RedisSyncClient
    if settings.REDIS_SENTINEL_SERVERS:
        RedisClass = RedisSentinelClient        # noqa  # NOSONAR
        connect_params = (
            settings.REDIS_SENTINEL_SERVERS,
            settings.REDIS_SENTINEL_NAME,
            settings.REDIS_SENTINEL_REDIS_DB,
            settings.REDIS_SENTINEL_REDIS_PASSWORD,
        )
    else:
        RedisClass = RedisClient
        connect_params = (settings.get_redis_server_url(),)

    redis_manager = RedisManager()

    # for cache
    redis_cache = RedisClass()
    await redis_cache.connect(*connect_params)
    redis_manager.add_cache_client(
        constants.DEFAULT_CACHE_CLIENT_NAME,
        redis_cache
    )

    # for sync client
    redis_sync_client = RedisSyncClient()
    await redis_sync_client.connect(*connect_params)
    redis_manager.add_cache_client(
        constants.REDIS_CLIENT_NAME_SYNC_CACHE,
        redis_sync_client
    )

    logger.info('startup-event: setup redis done')


async def setup_elasticsearch(settings: ElasticseaerchSetting):
    logger.info('startup-event: setup elasticsearch running...')
    from core.elk import ElasticsearchClient, ElasticsearchManager

    elasticsearch_manager = ElasticsearchManager()

    client = ElasticsearchClient(
        elastic_urls=settings.ELASTIC_SEARCH_URL,
        elastic_user=settings.ELASTIC_USER,
        elastic_password=settings.ELASTIC_PASSWORD,
        logtash_index=settings.ELASTIC_JOURNEY_LOGSTASH,
        kibana_url=settings.ELASTIC_KIBANA_URL
    )
    await client.connect()

    elasticsearch_manager.add_client(constants.DEFAULT_ELASTICSEARCH_CLIENT_NAME, client)

    logger.info('startup-event: setup elasticsearch done')
