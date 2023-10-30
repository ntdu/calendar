# -*- coding: utf-8 -*-
from engineio.async_drivers.asgi import WebSocket
from uvicorn.workers import UvicornWorker


# Overide Websocket to process pentest issue server/service disclosure
async def overide_call(self, environ):
    self.asgi_receive = environ['asgi.receive']
    self.asgi_send = environ['asgi.send']
    await self.asgi_send({'type': 'websocket.accept', 'headers': [(b'Server', b'SCC SOP')]})
    await self.handler(self)

WebSocket.__call__ = overide_call


class MyCustomUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        'headers': [
            ('server', 'SCC SOP')
        ],
        'server_header': False,
    }
