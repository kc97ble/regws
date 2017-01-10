#!/usr/bin/env python
from gevent.wsgi import WSGIServer
from regws import app

http_server = WSGIServer(('0.0.0.0', 5000), app)
http_server.serve_forever()
