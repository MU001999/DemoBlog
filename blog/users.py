# -*- coding: utf-8 -*-

import os
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *

app.secret_key = os.urandom(24)


@app.route('/login', methods=['POST'])
def login():
    username, password = request.form['username'], request.form['password']
    ans = check(username, password)
    if ans[1]:
        session['logged_in'] = True
        session['username'] = username
        session['password'] = password
        session['nickname'] = ans[0]
        return "success"
    else:
        return ans[0]


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('nickname', None)
    session['logged_in'] = False
    return "success"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('/users/signup.html')
    if check_exist(request.form['username']):
        return "error"

    if add_user(request.form['username'], request.form['password'], request.form['nickname']):
        session['logged_in'] = True
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['nickname'] = request.form['nickname']
        return "success"
    else:
        return "error"


@app.route('/editpwd', methods=['GET', 'POST'])
def edit_pwd():
    if request.method == 'GET':
        return render_template('/users/edit.html', see=False)

    u2n = request.form['password']
    update_user(session['username'], u2n, "pwd")
    session['password'] = u2n
    return redirect('/')


@app.route('/editnick', methods=['GET', 'POST'])
def edit_nick():
    if request.method == 'GET':
        return render_template('/users/edit.html', see=True)

    u2n = request.form['nickname']
    update_user(session['username'], u2n, "nick")
    session['nickname'] = u2n
    return redirect('/')


@app.route("/me")
def set_me():
    if session.get('logged_in', False):
        _ = get_articles_single_user(session['username'])
        __ = get_articles_single_user(session['username'])
        return render_template('/users/me.html', articles=_, _=__)
    else:
        return render_template('/users/me.html')


@app.route('/users/<username>')
def set_other(username):
    user = get_user(username)
    pos, arts = search_by_username(username)
    return render_template('/users/other.html', user=user, posts=pos, articles=arts)
