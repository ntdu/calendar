# -*- coding: utf-8 -*-
import logging
import time
from typing import Dict, Tuple
from uuid import uuid4

import ujson
from core import constants
from core.abstractions import AbsRedisMixin
from pydantic import BaseModel


class FChatCacheMixin(AbsRedisMixin):
    logger: logging.Logger
    client_id_map_livechat_id: Dict = {}

    async def fchat_get_client_info(self, client_id: str, **kwargs) -> Dict:
        _res = await self.slave_client.hget(constants.CACHE_FCHAT_CLIENT_INFO, client_id)
        if _res:
            # print(client_id, _res)
            res: Dict = ujson.loads(_res)
            if client_id not in self.client_id_map_livechat_id and 'live_chat_id' in res:
                self.client_id_map_livechat_id.update({
                    client_id: {
                        'live_chat_id': res.get('live_chat_id'),
                        'room_id': res.get('conversation_id'),
                        'at_time': int(time.time())
                    }
                })
            return res

    async def fchat_create_new_conversation(self, client_id: str, data: BaseModel, **kwargs):
        return await self.client.hset(
            constants.CACHE_FCHAT_CLIENT_INFO,
            client_id,
            data.json()
        )

    async def fchat_save_message(self, conversation_id: str, timestamp: int, message: str, **kwargs):
        if not isinstance(conversation_id, str) or not isinstance(timestamp, int) or not isinstance(message, str):
            self.logger.warning(f'NOT save message {conversation_id=} | {timestamp=} | {message=}')
            return
        return await self.client.hset(
            constants.CACHE_FCHAT_ROOM_MESSAGES.format(room_id=conversation_id),
            timestamp,
            message
        )

    async def fchat_get_conversation_messages(self, conversation_id: str, **kwargs):
        if not isinstance(conversation_id, str):
            self.logger.warning(f'NOT get message {conversation_id=}')
            return
        _res = await self.client.hgetall(
            constants.CACHE_FCHAT_ROOM_MESSAGES.format(room_id=conversation_id)
        )
        if _res:
            res = {}
            for k, v in _res.items():
                try:
                    res[k] = ujson.loads(v)
                except Exception:
                    res[k] = v
            return res
        else:
            return {}

    async def fchat_get_configs(self, live_chat_id: str, **kwargs):
        return await self.slave_client.hget(
            constants.CACHE_FCHAT_CONFIGS,
            live_chat_id
        )

    async def live_chat_get_agent_status(self, saleman_id: str, **kwargs):
        return await self.slave_client.hgetall(
            constants.CACHE_FCHAT_SALEMAN_STATUS.format(saleman_id=saleman_id),
        )

    async def fchat_check_saleman_online_status(self, saleman_id: str, **kwargs) -> bool:
        name = constants.CACHE_FCHAT_SALEMAN_ONLINE.format(saleman_id=saleman_id)
        saleman_online_sessions: Dict[str, Dict] = await self.slave_client.hgetall(name)
        expired_sids = []
        if saleman_online_sessions:
            for socket_id, raw_info in saleman_online_sessions.items():
                try:
                    info = ujson.loads(raw_info)
                    timestamp = info.get('timestamp')
                    if isinstance(timestamp, (int, float,)) and time.time() - timestamp <= 90:
                        return True
                    else:
                        expired_sids.append(socket_id)
                except Exception:
                    continue
                finally:
                    if expired_sids:
                        await self.client.hdel(name, *expired_sids)
        return False

    async def fchat_set_uploaded_attachment_for_grid_msg(
        self,
        room_id: str,
        grid_id: str,
        attachment: str,
        job_id: str = None,
        **kwargs
    ):
        if not job_id:
            job_id = str(uuid4())
        return await self.client.hset(
            constants.CACHE_FCHAT_ROOM_GRID_ATTACHMENTS.format(
                room_id=room_id,
                grid_id=grid_id
            ),
            job_id,
            attachment
        )

    async def fchat_get_uploaded_attachment_for_grid_msg(
        self,
        room_id: str,
        grid_id: str,
        **kwargs
    ):
        return await self.slave_client.hgetall(
            constants.CACHE_FCHAT_ROOM_GRID_ATTACHMENTS.format(
                room_id=room_id,
                grid_id=grid_id
            )
        )

    async def fchat_clear_uploaded_attachment_for_grid_msg(
        self,
        room_id: str,
        grid_id: str,
        **kwargs
    ):
        return await self.client.delete(
            constants.CACHE_FCHAT_ROOM_GRID_ATTACHMENTS.format(
                room_id=room_id,
                grid_id=grid_id
            )
        )

    async def fchat_verify_client(
        self,
        client_id: str,
        live_chat_id: str,
        **kwargs
    ) -> Tuple[bool, Dict]:
        if client_id in self.client_id_map_livechat_id:
            if live_chat_id == self.client_id_map_livechat_id[client_id].get('live_chat_id'):
                return True, self.client_id_map_livechat_id[client_id]
        client_info = await self.fchat_get_client_info(client_id, **kwargs)
        if client_info and live_chat_id == client_info.get('live_chat_id'):
            return True, self.client_id_map_livechat_id[client_id]
        return False, {}
