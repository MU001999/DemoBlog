# -*- coding: utf-8 -*-

import time
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route('/forum')
def set_forum():
    try:
        if session['logged_in']:
            posts = get_posts_recently()
            return render_template('/forum/forum.html', posts=posts)
    except:
        return redirect('/login')


@app.route('/forum/post/<int:order>')
def set_post(order):
    pass


@app.route('/forum/posts/write', methods=['GET', 'POST'])
def write_post():
    if request.method == 'GET':
        try:
            if session['logged_in']:
                return render_template('/forum/postPaste.html')
        except:
            return redirect('/login')
    title, lz, theme, content = request.form['title'], session['nickname'], request.form['theme'], request.form['content']
    username = session['username']
    plate = request.form['plate']
    time_post = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    post_id = add_post(title, lz, theme, content, time_post, username, plate)
    return redirect('/posts/' + str(post_id))


@app.route('/forum/plates/<name>')
def set_plate(name):
    pass
