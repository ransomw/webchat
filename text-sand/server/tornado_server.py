from os import path

from pdb import set_trace as st

import tornado.web

SCRIPT_DIR = path.dirname(path.realpath(__file__))
ASSETS_DIR = path.join(path.split(SCRIPT_DIR)[0], 'assets')

SECRET_KEY = 'mmmsecret'

GUEST_NAME = None

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
        print "guest name in get", GUEST_NAME
        if (GUEST_NAME is None
            and not self.get_cookie('guest')):
            self.render('knocker.html')
        elif self.get_cookie('guest'):
            self.render('knocker_wait.html')
        else:
            self.write("another guest is ahead of you")

    def post(self):
        print "guest name in post", GUEST_NAME
        if globals()['GUEST_NAME'] is not None:
            # security (call the cops)
            self.write(("you may not knock "
                        "if another guest is ahead of you"))
        else:
            GUEST_NAME = self.get_body_argument('guest_name')
            self.set_cookie('guest', 'is_guest')
            self.redirect('/knocker')

    def put(self):
        print "guest name in put", GUEST_NAME
        if not self.get_cookie('guest'):
            # security
            self.write("you are not the next guest")
        elif self.get_body_argument('action_type') == 'leave':
            st()
            GUEST_NAME = None
            self.set_cookie('guest', '')
            self.redirect('/knocker')

class PeepholeHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie('owner'):
            self.redirect('/keyhole')
        elif GUEST_NAME is not None:
            self.render('peephole_guest.html', guest_name=GUEST_NAME)
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
    (r"/knocker", KnockerHandler),
    (r"/peephole", PeepholeHandler),
    (r"/roomhole", RoomHandler),
    (r'/assets/(.*)', tornado.web.StaticFileHandler, {'path': ASSETS_DIR}),
])
