from os import path

import tornado.web

SCRIPT_DIR = path.dirname(path.realpath(__file__))
ASSETS_DIR = path.join(path.split(SCRIPT_DIR)[0], 'assets')

class KeyholeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("keyhole unimplemented")

class KnockerHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("knocker unimplemented")

class PeepholeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("peephole unimplemented")

class RoomHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("room unimplemented")

application = tornado.web.Application([
    (r"/keyhole", KeyholeHandler),
    (r"/", KnockerHandler),
    (r"/peephole", PeepholeHandler),
    (r"/roomhole", RoomHandler),
    (r'/assets/(.*)', tornado.web.StaticFileHandler, {'path': ASSETS_DIR}),
])
