"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)


from blog import articles, chat, codes, forum, index, play, users
