# -*- coding: utf-8 -*-

import os
import time
from flask import render_template, redirect, request, session, abort
from blog import app
from blog.link2db import *


@app.route('/articles/write', methods=['GET', 'POST'])
def paste_article():
    if request.method == 'GET':
        return render_template('/articles/edit.html', edit=False) if session.get('logged_in', False) else redirect('/login')

    title, author, content = request.form['title'], session['nickname'], request.form['content']
    labels = request.form['labels'].split(";")
    username = session['username']
    time_post = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    completed = request.form['completed'] == "1"
    post_id = add_article(title, author, content, time_post, username, labels, completed)
    return redirect('/articles/' + str(post_id))


@app.route('/articles/edit/<int:order>', methods=['GET', 'POST'])
def edit_article(order):
    if not session.get('logged_in', False):
        return redirect('/login')
    if request.method == 'GET':
        article = get_article(order)
        if session['username'] != article['username']:
            abort(404)
        return render_template('/articles/edit.html', edit=True, article=article, labels=';'.join(article['labels']))
    title, content, labels = request.form['title'], request.form['content'], request.form['labels'].split(";")
    completed = request.form['completed'] == "1"
    update_article(order, title, content, labels, completed)
    return redirect('/articles/' + str(order))


@app.route('/articles/<int:order>', methods=['GET', 'POST'])
def set_article(order):
    if request.method == 'GET':
        article = get_article(order)
        comments = get_comments(order, "articles")
        if session.get('username', None) != article['username'] and not article['completed']:
            abort(404)
        return render_template('/articles/article.html',
                               article=article,
                               comments=comments,
                               edit=(session.get('username', None) == article['username']))
    if not session.get('logged_in', False):
        return redirect('/login')

    cz = session['nickname']
    content = request.form['content']
    username = session['username']
    time_comment = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    add_comment_for_article(cz, content, username, time_comment, order)
    return redirect('/articles/' + str(order))


@app.route('/articles/all/<int:page_id>')
def set_articles(page_id=0):
    page_ids = range(max(0, min(page_id-2, articles.count()/10)), min(page_id+3, articles.count()/10))
    _articles = get_articles(page_id)
    return render_template('/articles/articles.html',
                           author="ALL AUTHORS",
                           articles=_articles,
                           pre=max(page_id-1, 0),
                           page_ids=page_ids,
                           next=min(articles.count(), page_id+1))


@app.route('/del/articles', methods=['POST'])
def del_articles():
    orders = request.form.getlist('do_delete')
    orders = map(lambda x: int(x), orders)
    del_articles_by_orders(orders)
    return redirect('/me')
