import logging
import pickle
from functools import partial
from datetime import datetime
from warnings import warn

from sockjs import MSG_OPEN
from sockjs import MSG_MESSAGE
from sockjs import MSG_CLOSE
from sockjs import MSG_CLOSED

from sockjs.protocol import (STATE_NEW, STATE_OPEN,
                             STATE_CLOSING, STATE_CLOSED)

import sockjs
from sockjs import Session as SessionBase
from sockjs import SessionManager as SessionManagerBase

from .my_redis import AioRedisEmitter
from .my_redis import CHANNEL as REDIS_CHANNEL

log = logging.getLogger('mysockjs')

def sock_js_state_str(state):
    if state == STATE_NEW:
        return 'new'
    if state == STATE_OPEN:
        return 'open'
    if state == STATE_CLOSING:
        return 'closing'
    if state == STATE_CLOSED:
        return 'closed'
    return 'UNKNOWN'

class SockjsSession(SessionBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = None
        self.redis = None

    def __repr__(self):
        return ('<SockjsSession ' + str(self) +
                ' state=' + sock_js_state_str(self.state) +
                ' username=' + self.username +
                '>')

    def close(self, *args, **kwargs):
        super().close(*args, **kwargs)
        log.debug("called close() on " + str(self))
        log.debug(str(args) + " " + str(kwargs))

    def expire(self, *args, **kwargs):
        super().expire(*args, **kwargs)
        log.debug("called expire() on " + repr(self))


def _session_factory(mgr, *args, **kwargs):
        session = SockjsSession(*args, **kwargs)
        session.redis = mgr.redis
        return session


class SockjsSessionManager(SessionManagerBase):
    """
    tack the aiohttp request onto the sockjs.Session as needed
    """

    def __init__(self,
                 get_username_from_request,
                 *args,
                 heartbeat_close=True,
                 **kwargs):
        super().__init__('chat_update', *args, **kwargs)
        self.factory = partial(_session_factory, self)
        self._get_username_from_request = get_username_from_request
        self._aioRedisEmitter = AioRedisEmitter(self)
        self._heartbeat_close = heartbeat_close

    def start(self):
        super().start()
        self._aioRedisEmitter.start()

    def get(self, *args, **kwargs):
        session = super().get(*args, **kwargs)
        request = kwargs.get('request', None)
        if session.username is None and request is not None:
            session.username = self._get_username_from_request(request)
        return session

    @property
    def redis(self):
        return self._aioRedisEmitter.redis


    async def _heartbeat_task(self):
        sessions = self.sessions

        if sessions:
            now = datetime.now()

            idx = 0
            while idx < len(sessions):
                session = sessions[idx]

                session._heartbeat()

                if self.debug:
                    log.debug("my heartbeat")
                    log.debug(str(sessions))
                    log.debug("session.expires: " +
                              str(session.expires) +
                              " now " + str(now) + " is " +
                              str(session.expires < now))
                    log.debug("1st bool " +
                              str(session.id in self.acquired) +
                              ", 2nd bool: " +
                              str(session.state == STATE_OPEN))

                if session.expires < now and self._heartbeat_close:
                    # Session is to be GC'd immedietely
                    if session.id in self.acquired:
                        await self.release(session)
                    if session.state == STATE_OPEN:
                        await session._remote_close()
                    if session.state == STATE_CLOSING:
                        await session._remote_closed()

                    del self[session.id]
                    del self.sessions[idx]
                    continue

                idx += 1

        self._hb_task = None
        self._hb_handle = self.loop.call_later(
            self.heartbeat, self._heartbeat)


async def sockjs_session_handler(msg, sess):
    """
    msg (sockjs.protocol.SockjsMessage):
      a collections.namedtuple with fields 'tp', 'data',
      where 'tp' is one of the 'MSG_*' types exported by sockjs
    sess (SockjsSession)
    """
    username = sess.username
    redis = sess.redis
    if msg.tp == sockjs.MSG_OPEN:
        log.debug("got open message")
        log.debug(username)
        sess.send('connected')
    elif msg.tp == sockjs.MSG_CLOSE:
        log.debug("got close message")
        log.debug(str(msg))
        if username and redis:
            log.debug("removing user from chat")
            await redis.hdel('users', username)
            await redis.publish(REDIS_CHANNEL, pickle.dumps({
                'username': username,
                'action': 'part',
            }))
        pass
    elif msg.tp == sockjs.MSG_CLOSED:
        log.debug("got closeD message")
        log.debug(str(msg))
        pass
    elif msg.tp == sockjs.MSG_MESSAGE:
        if msg.data == 'backbeat':
            pass
        else:
            warn(("unexpected message data from client side" +
                  repr(msg) + " for session " + repr(sess)))
    else:
        warn(("unexpected message (by type) from client side" +
                  repr(msg) + " for session " + repr(sess)))


async def sockjs_on_app_shutdown(app):
    """
    attach to the web.Application.on_shutdown signal
    to cleanup websockets on application shutdown
    http://aiohttp.readthedocs.io/en/stable/web_reference.html#aiohttp.web.Application.on_shutdown
    """
    session_manager = sockjs.get_manager('chat_update', app)
    await session_manager.clear()
    session_manager.stop()
