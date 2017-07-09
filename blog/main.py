from flask import render_template, redirect, request
from blog import app
from blog.link2db import *

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return None

@app.route('/signup')
def signup():
    return  render_template('signup.html', sth_wrong=False)

@app.route('/adduser', methods=['POST'])
def adduser():
    if check_exist(request.form['userid']):
        return render_template('/signup.html', sth_wrong=True)
    return redirect('/login')