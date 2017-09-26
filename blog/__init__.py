"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import blog.index
import blog.users
import blog.codes
