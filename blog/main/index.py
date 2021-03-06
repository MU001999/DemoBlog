# -*- coding: utf-8 -*-


import os
from flask import render_template, request, send_from_directory
from blog import app
from blog.link2db import *


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'imgs'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def hello():
    pos = get_posts_recently()
    arts = get_articles_recently()
    return render_template('/index/index.html',
                           posts=pos,
                           articles=arts)


@app.route('/search', methods=['POST'])
def search():
    target = request.form['target']
    us, pos, cods, arts = search_by_target(target)
    return render_template('/index/search.html',
                           users=us,
                           posts=pos,
                           codes=cods,
                           articles=arts)
