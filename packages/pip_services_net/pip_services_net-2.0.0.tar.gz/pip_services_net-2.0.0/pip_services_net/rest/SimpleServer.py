# -*- coding: utf-8 -*-
"""
    pip_services_net.rest.SimpleServer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Simple WSGI web server with shutdown hook
    from http://stackoverflow.com/questions/11282218/bottle-web-framework-how-to-stop
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
from bottle import WSGIRefServer

class SimpleServer(WSGIRefServer):
    def run(self, app): # pragma: no cover
        from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
        from wsgiref.simple_server import make_server
        import socket

        class FixedHandler(WSGIRequestHandler):
            def address_string(self): # Prevent reverse DNS lookups please.
                return self.client_address[0]
            def log_request(*args, **kw):
                if not self.quiet:
                    return WSGIRequestHandler.log_request(*args, **kw)

        handler_cls = self.options.get('handler_class', FixedHandler)
        server_cls  = self.options.get('server_class', WSGIServer)

        if ':' in self.host: # Fix wsgiref for IPv6 addresses.
            if getattr(server_cls, 'address_family') == socket.AF_INET:
                class server_cls(server_cls):
                    address_family = socket.AF_INET6

        srv = make_server(self.host, self.port, app, server_cls, handler_cls)
        self.srv = srv ### THIS IS THE ONLY CHANGE TO THE ORIGINAL CLASS METHOD!
        srv.serve_forever()

    def shutdown(self): ### ADD SHUTDOWN METHOD.
        # Wait because server run may not be active
        attempts = 100
        while attempts > 0:
            if hasattr(self, 'srv'):
                try:
                    self.srv.shutdown()
                except:
                    pass
                break
            attempts -= 1
            time.sleep(0.1)

        # self.server.server_close()
