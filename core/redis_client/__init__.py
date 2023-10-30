# -*- coding: utf-8 -*-

# monkey patch for redis@4.4.0
# from redis.asyncio.sentinel import SentinelManagedConnection
# from redis.exceptions import ConnectionError, ReadOnlyError, ResponseError, TimeoutError
# async def read_response(self, disable_decoding: bool = False, **kwarg):
#     try:
#         return await super(SentinelManagedConnection, self).read_response(disable_decoding=disable_decoding)
#     except ReadOnlyError:
#         if self.connection_pool.is_master:
#             # When talking to a master, a ReadOnlyError when likely
#             # indicates that the previous master that we're still connected
#             # to has been demoted to a slave and there's a new master.
#             # calling disconnect will force the connection to re-query
#             # sentinel during the next connect() attempt.
#             await self.disconnect()
#             raise ConnectionError("The previous master is now a slave")
#         raise
# SentinelManagedConnection.read_response = read_response

from .client import RedisClient, RedisSyncClient    # noqa
from .sentinel_client import RedisSentinelClient    # noqa
from .manager import RedisManager                   # noqa
