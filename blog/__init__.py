"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

from blog import users, codes, index, articles
