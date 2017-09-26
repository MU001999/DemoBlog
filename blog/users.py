# -*- coding: utf-8 -*-

import os
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *

app.secret_key = os.urandom(24)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        ans = check(username, password)
        if ans:
            session['logged_in'] = True
            session['username'], session['password'], session['nickname'] = username, password, ans
            return redirect('/')
        return render_template('login.html', sth_wrong=True)
    return render_template('login.html', sth_wrong=False)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('nickname', None)
    session['logged_in'] = False
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', sth_wrong=False)

    if check_exist(request.form['username']):
        return render_template('/signup.html', sth_wrong=True)

    if add_user(request.form['username'], request.form['password'], request.form['nickname']):
        session['logged_in'] = True

        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['nickname'] = request.form['nickname']

        return redirect('/')

    return render_template('signup.html', sth_wrong=True)
