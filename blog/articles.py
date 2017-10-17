# -*- coding: utf-8 -*-

import os
import time
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route('/articles/paste', methods=['GET', 'POST'])
def paste_article():
    if request.method == 'GET':
        try:
            if session['logged_in']:
                return render_template('articlePaste.html')
        except:
            return redirect('/login')
    title, author, content = request.form['title'], session['nickname'], request.form['content']
    time_post = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    post_id = add_article(title, author, content, time_post)
    return redirect('/articles/' + str(post_id))


@app.route('/articles/<int:article_id>', methods=['GET', 'POST'])
def set_article(article_id):
    title, author, content, post_time = get_article(article_id)
    return render_template('article.html', title=title, author=author, content=content, post_time=post_time)


@app.route('/articles/all/<int:page_id>')
def set_articles(page_id):
    page_ids = range(max(0, page_id-2), page_id)
