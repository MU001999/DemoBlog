# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route("/me")
def get_me():
    if not session['logged_in']:
        return redirect('/')
    return render_template('me.html')
