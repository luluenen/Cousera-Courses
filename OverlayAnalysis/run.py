# coding: utf-8
from app import app

from gevent.wsgi import WSGIServer
http_server = WSGIServer(('', 5001), app)
http_server.serve_forever()
app.run(debug=True, port=5001)

# Optional params:
#   host: Hostname to listen on. Defaults to 127.0.0.1 (localhost).
#       Set to ‘0.0.0.0’ to have server available externally.
#   port: Defaults to 5000.
