import re
import json
import asyncio
import pickle
from urllib.parse import urlparse

import redis
import aioredis

from flask import _app_ctx_stack
from flask import current_app

MSG_DATA_REGEXP = r'^([A-z]+):(.*)$'

CHANNEL = 'chat-events'

### threaded

def _connect_redis():
    """ return a new redis session """
    return redis.StrictRedis(host='localhost', port=6379, db=11)


def get_redis():
    top = _app_ctx_stack.top
    if not hasattr(top, 'redis_session'):
        top.redis_session = _connect_redis()
    return top.redis_session

### asyncio

def _parse_redis_url(url):
    p = urlparse(url)
    if p.scheme != 'redis':
        raise ValueError('Invalid redis url')
    if ':' in p.netloc:
        host, port = p.netloc.split(':')
        port = int(port)
    else:
        host = p.netloc or 'localhost'
        port = 6379
    if p.path:
        db = int(p.path[1:])
    else:
        db = 0
    if not host:
        raise ValueError('Invalid redis hostname')
    return host, port, db


class AioRedisEmitter(object):

    def __init__(self, session_manager,
                     url='redis://localhost:6379/11'):
        """
        * session_manager (sockjs.SessionManager)
        * url (str): the url of the redis database to connect
           to for pubsub updates.
        """
        self._session_manager = session_manager
        self._emitter_task = None
        self.redis = None
        self.host, self.port, self.db = _parse_redis_url(url)

    def _emitToSession(self, session_id, data):
        session = self._session_manager.get(session_id, None)
        if session is None:
            warn(("tried to emit to session, but didn't find "
                      "session id in session manager"))
            return
        session.send(json.dumps(data))

    async def _create_redis(self):
        redis = await aioredis.create_redis(
            (self.host, self.port),
            db=self.db,
        )
        return redis

    def start(self):
        if not self._emitter_task:
            self._emitter_task = asyncio.ensure_future(
                self._listen(),
                loop=self._session_manager.loop,
                )

    async def _listen(self):
        """
        create a separate connection for 'subscribe mode'
        """
        self.redis = await self._create_redis()
        sub = await self._create_redis()
        chan = (await sub.subscribe(CHANNEL))[0]
        while True:
            serialized_msg = await chan.get()
            self._broadcast(pickle.loads(serialized_msg))

    def _broadcast(self, data):
        self._session_manager.broadcast(json.dumps(data))
