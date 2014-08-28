#! /usr/bin/env python

from os import environ

PORT = int(environ.get('PORT', 3000))

#######
# copy 'n paste from standard library documentation
#######

import SimpleHTTPServer
import SocketServer

# PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()

########
