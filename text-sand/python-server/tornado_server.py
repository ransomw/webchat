from os import path

from pdb import set_trace as st

import tornado.web

SCRIPT_DIR = path.dirname(path.realpath(__file__))
ASSETS_DIR = path.join(path.split(SCRIPT_DIR)[0], 'assets')
TEMPLATE_DIR = path.join(path.split(SCRIPT_DIR)[0], 'views', 'server')

SECRET_KEY = 'mmmsecret'

APP_STATE = dict(
    guest_name=None,
    chatting=False,
    messages = []
)

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
        if (APP_STATE['guest_name'] is None
            and not self.get_cookie('guest')):
            self.render('knocker.html')
        elif self.get_cookie('guest'):
            if APP_STATE['chatting']:
                self.redirect('/room')
            else:
                self.render('knocker_wait.html')
        else:
            self.write("another guest is ahead of you")

    def post(self):
        action_type = self.get_body_argument(
            'action_type', default=None)
        if (APP_STATE['guest_name'] is not None
            and action_type is None):
            # security (call the cops)
            self.write(("you may not knock "
                        "if another guest is ahead of you"))
        elif action_type is not None:
            if action_type == 'leave':
                APP_STATE['guest_name'] = None
                self.set_cookie('guest', '')
                self.redirect('/knocker')
            else:
                self.write("unknown action type: " + action_type)
        else:
            APP_STATE['guest_name'] = self.get_body_argument('guest_name')
            self.set_cookie('guest', 'is_guest')
            self.redirect('/knocker')


class PeepholeHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie('owner'):
            self.redirect('/keyhole')
        elif APP_STATE['guest_name'] is not None:
            self.render('peephole_guest.html', guest_name=APP_STATE['guest_name'])
        else:
            self.render('peephole.html')

    def post(self):
        action_type = self.get_body_argument('action_type')
        if action_type == 'exit':
            self.set_cookie('owner', '')
            self.redirect('/keyhole')
        elif action_type == 'open':
            APP_STATE['chatting'] = True
            self.redirect('/room')
        else:
            raise Exception(("with owner at peephole, "
                             "unknown action type: ") + action_type)


class RoomHandler(tornado.web.RequestHandler):
    def get(self):
        if not APP_STATE['chatting']:
            if self.get_cookie('owner'):
                self.redirect('/peephole')
            else:
                self.redirect('/knocker')
        else:
            self.render('room.html')

    def post(self):
        action_type = self.get_body_argument('action_type')
        if action_type == 'stop':
            APP_STATE['chatting'] = False
            APP_STATE['messages'] = []
        self.redirect('/room') # rely on redirect in get

class RoomApiHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('\n'.join(map(lambda msg: msg[0] + ': ' + msg[1],
                                 APP_STATE['messages'])))

    def post(self):
        message = self.get_argument('message')
        if self.get_cookie('guest'):
            APP_STATE['messages'].append([APP_STATE['guest_name'], message])
        elif self.get_cookie('owner'):
            APP_STATE['messages'].append(['X', message])




application = tornado.web.Application([
    (r"/keyhole", KeyholeHandler),
    (r"/", KnockerHandler),
    (r"/knocker", KnockerHandler),
    (r"/peephole", PeepholeHandler),
    (r"/room", RoomHandler),
    (r"/room/api", RoomApiHandler),
    (r'/assets/(.*)', tornado.web.StaticFileHandler, {'path': ASSETS_DIR}),
], template_path=TEMPLATE_DIR)
