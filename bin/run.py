import sys
import os
import re

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

wcapp.socketio.run(wcapp.app, host='0.0.0.0', port=PORT,
                       debug=False)
