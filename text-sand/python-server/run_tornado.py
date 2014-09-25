#! /usr/bin/env python

from os import environ

import tornado.ioloop

from tornado_server import application

PORT = int(environ.get('PORT', 3000))

if __name__ == "__main__":
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
