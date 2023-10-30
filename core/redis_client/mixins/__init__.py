# -*- coding: utf-8 -*-
from .fchat_cache_mixin import FChatCacheMixin          # noqa
from .redis_pubsub_mixin import RedisPubSubMixin        # noqa


class DefaultMixins(
    FChatCacheMixin,
    RedisPubSubMixin
):
    pass
