
import os

from flask import Flask

from flask_socketio import SocketIO
from flask_socketio import emit
import eventlet

from wcapp import config


_SETTINGS_ENV_VAR = 'WEBCHAT_FLASK_SETTINGS'
_PROJ_ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '..', '..', '..')
)

app = Flask(
    __name__,
    static_folder=os.path.join(_PROJ_ROOT_DIR, 'build', 'server_static')
)

if os.environ.get(_SETTINGS_ENV_VAR):
    app.config.from_envvar(_SETTINGS_ENV_VAR)
else:
    app.config.from_object(config)

eventlet.monkey_patch(
    all=False,
    os=True,
    select=True,
    socket=True,
    # patching the threading module breaks
    # sqlalchemy's scoped_session
    thread=True,
    time=True,
)
socketio = SocketIO(
    async_mode='eventlet',
)

@socketio.on('connect')
def _on_connect():
    # print("socketio connect")
    emit('connected', {'data': 'Connected'})


@socketio.on('disconnect')
def _on_disconnect():
    # print("socketio disconnect")
    pass


socketio.init_app(
    app,
    message_queue='redis://localhost:6379/11',
)

def new_message_handler(message_object):
    socketio.emit('new message', message_object)


import wcapp.views
from wcapp.view_helpers import add_message
from wcapp.my_redis import get_redis
from wcapp.my_redis import get_new_msg_chan

with app.app_context():
    get_redis().delete('users')
    get_redis().delete('messages')
    add_message('system', "welcome to the chat <3")
    socketio.server.start_background_task(
        get_new_msg_chan().thread)
    get_new_msg_chan().add_handler(new_message_handler)
