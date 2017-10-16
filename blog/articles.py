# -*- coding: utf-8 -*-

import os
from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route('/articles/paste', methods=['GET', 'POST'])
def paste_article():
    if request.method == 'GET':
        return render_template('articlePaste.html')
    pass


@app.route('/article/<int:article_id>', methods=['GET', 'POST'])
def set_article(article_id):
    title, author, content = get_article(article_id)
    return render_template('article.html', title=title, author=author, content=content)
