#! /usr/bin/env python

from os import environ
from os import path

PORT = int(environ.get('PORT', 3000))
SCRIPT_DIR = path.dirname(path.realpath(__file__))
ASSETS_DIR = path.join(path.split(SCRIPT_DIR)[0], 'assets')

import tornado.ioloop
import tornado.web

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", HelloHandler),
    (r'/assets/(.*)', tornado.web.StaticFileHandler, {'path': ASSETS_DIR}),
])

if __name__ == "__main__":
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
