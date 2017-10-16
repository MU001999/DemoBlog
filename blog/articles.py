# -*- coding: utf-8 -*-

import os
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
    post_id = add_article(title, author, content)
    return redirect('/articles/' + str(post_id))


@app.route('/articles/<int:article_id>', methods=['GET', 'POST'])
def set_article(article_id):
    title, author, content = get_article(article_id)
    return render_template('article.html', title=title, author=author, content=content)
