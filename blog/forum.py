# -*- coding: utf-8 -*-

import time
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route('/forum')
def set_forum():
    return render_template('/forum/forum.html', posts=get_posts_recently(), name="Forum's Homepage")\
        if session.get('logged_in', False) else redirect('/login')


@app.route('/forum/posts/<int:order>', methods=['GET', 'POST'])
def set_post(order):
    if request.method == 'GET':
        post = get_post(order)
        comments = get_comments(order)
        return render_template('/forum/post.html', post=post, comments=comments, order=order)
    else:
        cz, content, username, time_comment = session['nickname'], request.form['content'], session['username'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        add_comment(cz, content, username, time_comment, order)
        return redirect('/forum/posts/' + str(order))


@app.route('/forum/posts/write', methods=['POST'])
def write_post():
    title, lz, content, plate = request.form['title'], session['nickname'], request.form['content'], request.form['plate']
    username = session['username']
    time_post = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    post_id = add_post(title, lz, content, time_post, plate, username)
    return redirect('forum/posts/' + str(post_id))


@app.route('/forum/plates/<name>')
def set_plate(name):
    return render_template('/forum/forum.html', name=name, posts=get_posts_by_plate(name))
