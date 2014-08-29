#! /usr/bin/env python

# from pdb import set_trace as st

from os import environ
from os import path

PORT = int(environ.get('PORT', 3000))
SCRIPT_DIR = path.dirname(path.realpath(__file__))

ASSETS_DIR = path.join(path.split(SCRIPT_DIR)[0], 'assets')

import SimpleHTTPServer

# class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
#     def list_directory(self, req_path):
#         print "got request path", req_path
#         st()
#         try:
#             list = os.listdir(path.join(ASSETS_DIR, req_path))
#         except os.error:
#             self.send_error(404, "No permission to list directory")
#             return None
#         list.sort(key=lambda a: a.lower())
#         f = StringIO()
#         #### removed line from default implementation
#         # displaypath = cgi.escape(urllib.unquote(self.path))
#         ####
#         displaypath = cgi.escape(urllib.unquote(ASSETS_DIR))
#         f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
#         f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
#         f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
#         f.write("<hr>\n<ul>\n")
#         for name in list:
#             fullname = os.path.join(path, name)
#             displayname = linkname = name
#             ##### extra line from stack overflow example
#             # date_modified = time.ctime(os.path.getmtime(fullname))
#             #####
#             # Append / for directories or @ for symbolic links
#             if os.path.isdir(fullname):
#                 displayname = name + "/"
#                 linkname = name + "/"
#             if os.path.islink(fullname):
#                 displayname = name + "@"
#                 # Note: a link to a directory displays with @ and links with /
#             f.write('<li><a href="%s">%s - %s</a>\n'
#                     % (urllib.quote(linkname), cgi.escape(displayname), date_modified))
#         f.write("</ul>\n<hr>\n</body>\n</html>\n")
#         length = f.tell()
#         f.seek(0)
#         self.send_response(200)
#         encoding = sys.getfilesystemencoding()
#         self.send_header("Content-type", "text/html; charset=%s" % encoding)
#         self.send_header("Content-Length", str(length))
#         self.end_headers()
#         return f

#######
# copy 'n paste from standard library documentation
#######


import SocketServer

# PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)
# httpd = SocketServer.TCPServer(("", PORT), MyHandler)

print "serving at port", PORT
httpd.serve_forever()

########
