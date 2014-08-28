#! /usr/bin/env python

#######
# copy 'n paste from standard library documentation
#######

import SimpleHTTPServer
import SocketServer

PORT = 3000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()

########
