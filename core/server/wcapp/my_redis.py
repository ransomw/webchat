import re

import redis

from flask import _app_ctx_stack
from flask import current_app

from wcapp import app

MSG_DATA_REGEXP = r'^([A-z]+):(.*)$'

class _NewMsgChanRedis(object):
    """ notification for new messages via redis """

    THREAD_SLEEP_TIME = 0.005

    def __init__(self, redis_session):
        self._handlers = {}
        self._pubsub_inst = redis_session.pubsub()
        self._pubsub_inst.subscribe(**{
            'new-messages': self._handle_new_messages})
        self._redis_session = redis_session
        self._thread_started = False

    def _handle_new_messages(self, message):
        msg = message['data'].decode('utf-8')
        msg_match_obj = re.match(MSG_DATA_REGEXP, msg)
        for handler in self._handlers.values():
            handler({
                'username': msg_match_obj.group(1),
                'msg': msg_match_obj.group(2),
                })
        # return {
        #     'username': msg_match_obj.group(1),
        #     'msg': msg_match_obj.group(2),
        #     }

    def add_handler(self, handler, name=None):
        if name is None:
            name = handler.__name__
        self._handlers[name] = handler

    def remove_handler(self, handler, silent=False):
        if isinstance(str(), handler):
            name = handler.__name__
        else:
            name = handler
        if silent:
            self._handlers.pop(name, None)
        else:
            self._handlers.pop(name)

    def pub_new_message(self, message):
        self._redis_session.publish('new-messages', message)

    def thread(self):
        if self._thread_started:
            return
        self._thread_started = True
        for msg_obj in self._pubsub_inst.listen():
            print("'thread' got message", msg_obj)
            pass
        self._thread_started = False


def _connect_redis():
    """ return a new redis session """
    return redis.StrictRedis(host='localhost', port=6379, db=1)


def get_redis():
    top = _app_ctx_stack.top
    if not hasattr(top, 'redis_session'):
        top.redis_session = _connect_redis()
    return top.redis_session


def get_new_msg_chan():
    top = _app_ctx_stack.top
    if not hasattr(top, 'new_msg_chan'):
        top.new_msg_chan = _NewMsgChanRedis(get_redis())
    return top.new_msg_chan
