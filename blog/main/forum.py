# -*- coding: utf-8 -*-

import time
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route('/forum')
def set_forum():
    if session.get('logged_in', False):
        return render_template('/forum/forum.html',
                               posts=get_posts_recently(),
                               name="Forum's Homepage",
                               user=get_user(session['username']))
    return render_template('/forum/forum.html',
                           posts=get_posts_recently(),
                           name="Forum's Homepage")


@app.route('/forum/posts/<int:order>', methods=['GET', 'POST'])
def set_post(order):
    if request.method == 'GET':
        post = get_post(order)
        comments = get_comments(order, "posts")
        return render_template('/forum/post.html', post=post, comments=comments)
    cz, content, username, time_comment = session['nickname'], request.form['content'], session['username'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    add_comment_for_post(cz, content, username, time_comment, order)
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
    if session.get('logged_in', False):
        return render_template('/forum/forum.html',
                               posts=get_posts_by_plate(name),
                               name=name,
                               user=get_user(session['username']))
    return render_template('/forum/forum.html',
                           posts=get_posts_by_plate(name),
                           name=name)
