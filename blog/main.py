import os
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')


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


@app.route('/signup')
def signup():
    return  render_template('signup.html', sth_wrong=False)


@app.route('/adduser', methods=['POST'])
def add_user():
    if check_exist(request.form['username']):

        return render_template('/signup.html', sth_wrong=True)

    if add_user(request.form['username'], request.form['password'], request.form['nickname']):

        session['logged_in'] = True

        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['nickname'] = request.form['nickname']

        return redirect('/')

    return render_template('signup.html', sth_wrong=True)


@app.route('/codes/paste', methods=['POST'])
def paste_code():
    return render_template('code.html')


@app.route('/codes/<int:code_id>')
def get_code(code_id):
    return render_template('code.html')