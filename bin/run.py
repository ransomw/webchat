import sys
import os
import re
import asyncio

from aiohttp import web as aioweb

PROJ_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)

SERVER_DIR = os.path.join(PROJ_ROOT, 'core', 'server')

sys.path.append(SERVER_DIR)
import wcapp

PORT = 5000

try:
    PORT = int(os.environ['PORT'])
except KeyError:
    pass
except ValueError as err:
    print(("got invalid port number '" +
           re.sub(r'.*\'(.*)\'.*', '\\1', err.args[0]) + "'"),
          file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    aio_app = wcapp.init_aiohttp_app(loop)

    # handler = aio_app.make_handler()
    # srv = loop.run_until_complete(
    #     loop.create_server(
    #         handler,
    #         '0.0.0.0',
    #         PORT,
    #     ))
    # print("serving on", srv.sockets[0].getsockname())
    # try:
    #     loop.run_forever()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     srv.close()
    #     loop.run_until_complete(srv.wait_closed())
    #     loop.run_until_complete(aio_app.shutdown())
    #     loop.run_until_complete(handler.shutdown(_HANDLER_SHUTDOWN_SEC))
    #     loop.run_until_complete(aio_app.cleanup())
    #     loop.close()

    aioweb.run_app(aio_app,
                   host='localhost',
                   port=PORT,
                   loop=loop,
    )
