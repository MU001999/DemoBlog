# -*- coding: utf-8 -*-

import os
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')