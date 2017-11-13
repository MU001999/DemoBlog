# -*- coding: utf-8 -*-

"""
This script runs the blog application using a development server.
"""

from os import environ
from blog import app, socketio

if __name__ == "__main__":
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('SERVER_HOST', '5555'))
    except ValueError:
        PORT = 5555
    socketio.run(app, debug=True, host=HOST, port=PORT)
