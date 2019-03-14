import os
import sys
import logging
from urllib.parse import urlsplit
from datetime import timedelta

from flask import Flask
from aiohttp import web as aioweb
from aiohttp_wsgi import WSGIHandler
import sockjs

from wcapp import config
from .sockjs_sess_mgr import SockjsSessionManager
from .sockjs_sess_mgr import sockjs_session_handler
from .sockjs_sess_mgr import sockjs_on_app_shutdown
from .views import blueprint

_SETTINGS_ENV_VAR = 'WEBCHAT_FLASK_SETTINGS'
_PROJ_ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '..', '..', '..')
)

_sockjsLogger = logging.getLogger('sockjs')
_sockjsLogger.setLevel(logging.DEBUG)
_sockjsLogger.addHandler(logging.StreamHandler(sys.stdout))

_mysockjsLogger = logging.getLogger('mysockjs')
_mysockjsLogger.setLevel(logging.DEBUG)
_mysockjsLogger.addHandler(logging.StreamHandler(sys.stdout))

def _aiohttp_request_2_wsgi_environ(request):
    """
    lifted from `engineio`
    dupe (functionality):  aiohttp_wsgi
    """
    message = request._message
    payload = request._payload

    uri_parts = urlsplit(message.path)
    environ = {
        'wsgi.input': payload,
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.async': True,
        'wsgi.multithreaded': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'SERVER_SOFTWARE': 'aiohttp',
        'REQUEST_METHOD': message.method,
        'QUERY_STRING': uri_parts.query or '',
        'RAW_URI': message.path,
        'SERVER_PROTOCOL': 'HTTP/%s.%s' % message.version,
        'REMOTE_ADDR': '127.0.0.1',
        'REMOTE_PORT': '0',
        'SERVER_NAME': 'aiohttp',
        'SERVER_PORT': '0',
        'aiohttp.request': request,
    }

    for hdr_name, hdr_value in message.headers.items():
        hdr_name = hdr_name.upper()
        if hdr_name == 'CONTENT-TYPE':
            environ['CONTENT_TYPE'] = hdr_value
            continue
        if hdr_name == 'CONTENT-LENGTH':
            environ['CONTENT_LENGTH'] = hdr_value
            continue

        key = 'HTTP_%s' % hdr_name.replace('-', '_')
        if key in environ:
            hdr_value = '%s,%s' % (environ[key], hdr_value)

        environ[key] = hdr_value

    environ['wsgi.url_scheme'] = environ.get('HTTP_X_FORWARDED_PROTO',
                                             'http')

    path_info = uri_parts.path
    environ['PATH_INFO'] = path_info
    environ['SCRIPT_NAME'] = ''

    return environ


def _get_username_from_flask_app_and_wsgi_environ(
        flask_app,
        environ,
):
    return flask_app.open_session(
        flask_app.request_class(environ)
    ).get('username', None)


def init_flask_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(
            _PROJ_ROOT_DIR, 'build', 'server_static'),
    )

    if os.environ.get(_SETTINGS_ENV_VAR):
        app.config.from_envvar(_SETTINGS_ENV_VAR)
    else:
        app.config.from_object(config)

    app.register_blueprint(
        blueprint,
        url_prefix='/',
    )

    return app


def init_aiohttp_app(loop):
    flask_app = init_flask_app()

    from wcapp.view_helpers import add_message
    from wcapp.my_redis import get_redis

    with flask_app.app_context():
        get_redis().delete('users')
        get_redis().delete('messages')
        add_message('system', "welcome to the chat <3")

    def _get_username_from_aiohttp_request(request):
        environ = _aiohttp_request_2_wsgi_environ(request)
        return _get_username_from_flask_app_and_wsgi_environ(
            flask_app, environ)


    app = aioweb.Application(loop=loop)

    sockjs_session_manager = SockjsSessionManager(
        _get_username_from_aiohttp_request,
        app,
        sockjs_session_handler,
        app.loop,
        heartbeat=3.0,
        timeout=timedelta(seconds=10),
        heartbeat_close=True,
        debug=False,
    )
    sockjs.add_endpoint(
        app,
        sockjs_session_handler,
        name=sockjs_session_manager.name,
        prefix='/sockjs', # default
        manager=sockjs_session_manager,
    )
    app.on_shutdown.append(sockjs_on_app_shutdown)

    #### must attach socket stuffs before the WSGI handler's glob
    app.router.add_route(
        "*", "/{path_info:.*}",
        WSGIHandler(flask_app.wsgi_app))
    return app
