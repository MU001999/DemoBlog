# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route("/me")
def get_me():
    try:
        if session['logged_in']:
            articles = get_articles_single_user(session['username'])
            return render_template('me.html', articles=articles)
    except:
        return redirect('/login')
