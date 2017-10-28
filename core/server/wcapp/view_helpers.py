"""
encapsulate persistance and external state mechanisms
such as databases and message queues
"""

import re

from wcapp.my_redis import get_redis
from wcapp.my_redis import get_new_msg_chan
from wcapp.my_redis import MSG_DATA_REGEXP

RE_USERNAME = r'^[A-z]+$'


class ViewHelperError(Exception):

    def get_client_msg(self):
        return "server error: " + (
            self.args[0] if len(self.args) > 0 else
            "unspecified")


def get_usernames():
    return [bytes_username.decode() for bytes_username in
            get_redis().lrange('users', 0, -1)]


def get_users():
    usernames = get_usernames()
    return [{'username': username} for username in usernames]


def get_messages():
    msg_strs = [bytes_username.decode() for bytes_username in
                get_redis().lrange('messages', 0, -1)]
    msg_match_objs = [re.match(MSG_DATA_REGEXP, msg)
                      for msg in msg_strs]
    json_msgs = [{
        'username': mo.group(1),
        'msg': mo.group(2)
    } for mo in msg_match_objs]
    return json_msgs


def user_join(username):
    if re.match(RE_USERNAME, username) is None:
        raise ViewHelperError("username may only contain letters")
    current_users = get_usernames()
    if username in current_users:
        raise ViewHelperError("this username already registered")
    if username == 'system':
        raise ViewHelperError("'system' is a reserved username")
    get_redis().rpush('users', username)


def add_message(username, msg_str):
    current_users = get_usernames()
    if username not in current_users and username != 'system':
        raise ViewHelperError(("got message from unregistered username"))
    message = username + ':' + msg_str
    get_redis().rpush('messages', message)
    get_new_msg_chan().pub_new_message(message)
