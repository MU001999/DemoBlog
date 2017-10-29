# -*- coding: utf-8 -*-


from flask import render_template, redirect, request, session
from blog import app
from blog.link2db import *


@app.route('/')
def hello():
    pos = get_posts_recently()
    arts = get_articles(0)
    return render_template('/index/index.html', posts=pos, articles=arts)


@app.route('/search', methods=['POST'])
def search():
    target = request.form['target']
    us, pos, cods, arts = search_by_target(target)
    return render_template('/index/search.html', users=us, posts=pos, codes=cods, articles=arts)
