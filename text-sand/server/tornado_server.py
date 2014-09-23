from os import path

from pdb import set_trace as st

import tornado.web

SCRIPT_DIR = path.dirname(path.realpath(__file__))
ASSETS_DIR = path.join(path.split(SCRIPT_DIR)[0], 'assets')

SECRET_KEY = 'mmmsecret'

class KeyholeHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie('owner'):
            self.render('keyhole.html')
        else:
            self.redirect('/peephole')

    def post(self):
        attempted_key = self.get_body_argument('secret_key')
        if attempted_key == SECRET_KEY:
            # set cookie to any truthy value
            self.set_cookie('owner', 'is_owner')
            self.redirect('/peephole')
        else:
            self.write("got incorrect key '" + attempted_key + "'")

class KnockerHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("knocker unimplemented")

class PeepholeHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie('owner'):
            self.redirect('/keyhole')
        else:
            self.render('peephole.html')

    def post(self):
        action_type = self.get_body_argument('action_type')
        if action_type == 'exit':
            self.set_cookie('owner', '')
            self.redirect('/keyhole')
        elif action_type == 'open':
            self.write("open door to guest unimplemented")
        else:
            raise Exception(("with owner at peephole, "
                             "unknown action type: ") + action_type)


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
