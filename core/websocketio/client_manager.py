# -*- coding: utf-8 -*-
import logging
import time
from typing import Dict

import socketio
from core import constants
from core.abstractions import AbsRedisClient, AbsRedisManager, SingletonClass

CLIENT_ID = 'client_id'
TIMESTAMP = 'timestamp'


class SocketClientManager(SingletonClass):
    redis_client: AbsRedisClient = None
    redis_manager: AbsRedisManager = None
    socketio_ins: socketio.AsyncServer = None

    def _singleton_init(self, **kwargs):
        self._sid_and_client_mapping: Dict[str, Dict] = {}
        # for example
        # {socket_id: {client_id: client_id, timestamp: int}}

        self._client_and_sid_mapping: Dict[str, Dict] = {}
        # for example
        # {client_id: {socket_id: timestamp}}
        # {'306a24a8-1a2b-11ed-b8db-0242c0a80103': {j_Y9bM8n7KKT5fUfAAAB: 1666077199}}

        self.logger = kwargs.get(constants.LOGGER) or logging.getLogger(constants.CONSOLE_LOGGER)

    def set_socketio_instance(self, sio: socketio.AsyncServer):
        self.socketio_ins = sio
        self.logger.info(f'{self.__class__.__name__} set {self.socketio_ins=} ')

    def set_redis_client(self, redis_client: AbsRedisClient):
        self.redis = redis_client
        self.logger.info(f'{self.__class__.__name__} set {self.redis=} ')

    def set_redis_manager(self, redis_manager: AbsRedisManager):
        self.redis_manager = redis_manager
        self.logger.info(f'{self.__class__.__name__} set {self.redis_manager=} ')

    async def clear_expired_mapping(self):
        clear_sids = []
        for k, v in self._sid_and_client_mapping.items():
            if v.get(TIMESTAMP) and time.time() - v.get(TIMESTAMP) > 3 * 24 * 3600:
                clear_sids.append(k)

        for sid in clear_sids:
            del self._sid_and_client_mapping[sid]

    async def clear_disconnected_client(self, socket_id: str):
        if not socket_id:
            return

        client_info = self._sid_and_client_mapping.get(socket_id)
        if client_info:
            client_id = client_info.get(CLIENT_ID)
            if client_id in self._client_and_sid_mapping:
                del self._client_and_sid_mapping[client_id][socket_id]
            del self._sid_and_client_mapping[socket_id]
            self.logger.info(
                'clear_disconnected_client',
                extra={
                    'client_id': client_id,
                    'socket_id': socket_id
                }
            )
            return client_id

    async def add_connected_client(self, socket_id: str, client_id: str):
        if not socket_id or not client_id:
            return

        if client_id not in self._client_and_sid_mapping:
            self._client_and_sid_mapping[client_id] = {}

        self._client_and_sid_mapping[client_id].update({socket_id: int(time.time())})
        self._sid_and_client_mapping[socket_id] = {
            CLIENT_ID: client_id,
            TIMESTAMP: int(time.time())
        }
        self.logger.info(
            'add_connected_client',
            extra={
                'client_id': client_id,
                'socket_id': socket_id
            }
        )

    async def send_to_socketio_client(self, client_id: str, event: str, message: Dict):
        socket_ids: Dict = self._client_and_sid_mapping.get(client_id)
        disconnected_socket_ids = []
        # self.logger.info(f'send_to_socketio_client {socket_ids=}')
        if socket_ids:
            for sid in socket_ids:
                if self.socketio_ins.manager.is_connected(sid, '/'):
                    await self.socketio_ins.emit(event, message, sid)
                    self.logger.info(
                        'send_to_socketio_client',
                        extra={
                            'client_id': client_id,
                            'sid': sid,
                            'event': event,
                            'message_data': message
                        }
                    )
                else:
                    disconnected_socket_ids.append(sid)

            # remove from connected client
            for dsid in disconnected_socket_ids:
                del self._client_and_sid_mapping[client_id][dsid]
                self.logger.warning(
                    'found_disconnected_client',
                    extra={
                        'client_id': client_id,
                        'sid': dsid,
                    }
                )
