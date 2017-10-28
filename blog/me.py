# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route("/me")
def get_me():
    if session.get('logged_in', False):
        _ = get_articles_single_user(session['username'])
        __ = get_articles_single_user(session['username'])
        return render_template('/users/me.html', articles=_, _=__)
    else:
        return redirect('/login')
