# -*- coding: utf-8 -*-

import os
from flask import render_template, redirect, request, session
from werkzeug.utils import secure_filename
from blog import app
from blog.link2db import *

app.secret_key = os.urandom(24)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/login', methods=['POST'])
def login():
    username, password = request.form['username'], request.form['password']
    ans = check(username, password)
    if ans[1]:
        user = get_user(username)
        session['logged_in'] = True
        session['username'] = username
        session['password'] = password
        session['nickname'] = ans[0]
        session['avatar'] = user['avatar']
        return "success"
    else:
        return ans[0]


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('nickname', None)
    session.pop('avatar')
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


@app.route('/edit', methods=['GET'])
def edit():
    if request.method == 'GET':
        return render_template('/users/edit.html',
                               user=get_user(session['username']))


@app.route('/editavatar', methods=['POST'])
def edit_avatar():
    f = request.files['file']
    if f and allowed_file(f.filename):
        if not os.path.isdir(os.path.join('blog', 'static', 'imgs', 'users', session['username'])):
            os.mkdir(os.path.join('blog', 'static', 'imgs', 'users', session['username']))
        file_name = os.path.join('blog', 'static', 'imgs', 'users', session['username'], secure_filename(f.filename))
        f.save(file_name)
        update_user(session['username'], os.path.join(session['username'], f.filename), "avatar")
    return redirect('/edit')


@app.route('/editinfo', methods=['POST'])
def edit_info():
    u2n = list()
    u2n.append(request.form['nickname'])
    u2n.append(request.form.get('sign', ""))
    update_user(session['username'], u2n, "info")
    session['nickname'] = u2n[0]
    return redirect('/edit')


@app.route('/editpwd', methods=['POST'])
def edit_pwd():
    u2n = request.form['password']
    update_user(session['username'], u2n, "pwd")
    session['password'] = u2n
    return redirect('/edit')


@app.route("/me")
def set_me():
    if session.get('logged_in', False):
        _ = get_articles_single_user(session['username'])
        __ = get_articles_single_user(session['username'])
        return render_template('/users/me.html', user=get_user(session['username']), articles=_, _=__)
    else:
        return render_template('/users/me.html')


@app.route('/users/<username>')
def set_other(username):
    user = get_user(username)
    pos, arts = search_by_username(username)
    return render_template('/users/other.html',
                           user=user,
                           posts=pos,
                           articles=arts)
