"""
The flask application package.
"""

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


from blog import articles, chat, codes, forum, index, play, users
