#!/usr/bin/python

from six.moves import SimpleHTTPServer, socketserver
import socket
from metaparticle_pkg.metaparticle import containerize

OK = 200

port = 8080

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(OK)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Hello Metparticle [{}] @ {}\n".format(self.path, socket.gethostname()).encode('UTF-8'))
        print("request for {}".format(self.path))
    def do_HEAD(self):
        self.send_response(OK)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

@containerize(
    'docker.io/brendanburns',
    options={
        'name': 'my-image',
        'runner': 'metaparticle',
        'replicas': 4,
        'ports': [8080],
        'publish': True
    })
def main():
    Handler = MyHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    httpd.serve_forever()

if __name__ == '__main__':
    main()
