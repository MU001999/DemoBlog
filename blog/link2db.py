# -*- coding: utf-8 -*-
import pymongo


conn = pymongo.MongoClient('localhost', 27017)
db = conn.demoblog

users = db.users
codes = db.codes
articles = db.articles
posts = db.posts

articles_sorted = articles.find({"type": "article"}).sort("order", pymongo.DESCENDING)


# common
def get_comments(order, col):
    return eval(col).find({'type': 'comment', 'order': order}).sort('corder')


# for users
def check(username, password):
    if users.find_one({"username": username, 'password': password}):
        return users.find_one({"username": username, 'password': password})['nickname'], True
    elif users.find_one({"username": username}):
        return "password", False
    else:
        return "username", False


def check_exist(username):
    if users.find_one({"username": username}):
        return True
    return False


def add_user(username, password, nickname):
    try:
        users.insert_one({'username': username, 'password': password, 'nickname': nickname})
        return True
    except:
        raise False


def update_user(username, u2n, info):
    if info == "pwd":
        users.update({"username": username}, {"$set": {"password": u2n}})
    elif info == "nick":
        global articles_sorted
        users.update({"username": username}, {"$set": {"nickname": u2n}}, multi=True)
        articles.update({"username": username}, {"$set": {"author": u2n}}, multi=True)
        posts.update({"username": username}, {"$set": {"lz": u2n}}, multi=True)
        articles_sorted = articles.find({"type": "article"}).sort("order", pymongo.DESCENDING)


def get_user(username):
    return users.find_one({'username': username})


# for codes
def add_code(poster, syntax, content):
    try:
        order = codes.find().count()
        codes.insert_one({'poster': poster, 'syntax': syntax, 'content': content, 'order': order})
        return order
    except MemoryError:
        raise MemoryError


def get_code(order):
    code = codes.find_one({"order": order})
    return code['poster'], code['syntax'], code['content']


# for articles
def add_article(title, author, content, time_post, username, labels, completed):
    global articles_sorted
    try:
        order = articles.find().count()
        articles.insert_one({'order': order,
                             'type': 'article',
                             'title': title,
                             'author': author,
                             'content': content,
                             'time_post': time_post,
                             'username': username,
                             'labels': labels,
                             'completed': completed})
        articles_sorted = articles.find({"type": "article"}).sort("order", pymongo.DESCENDING)
        return order
    except MemoryError:
        raise MemoryError


def update_article(order, title, content, labels, completed):
    global articles_sorted
    articles.update({"order": order, "type": "article"},
                    {"$set": {"title": title, "content": content, "labels": labels, "completed": completed}})
    articles_sorted = articles.find({"type": "article"}).sort("order", pymongo.DESCENDING)


def add_comment_for_article(cz, content, username, time_comment, order):
    corder = articles.find({'order': order, 'type': 'comment'}).count() + 1
    articles.insert_one({'order': order,
                         'corder': corder,
                         'type': 'comment',
                         'cz': cz,
                         'content': content,
                         'username': username,
                         'time_comment': time_comment})


def get_article(article_id):
    article = articles.find_one({'order': article_id, "type": "article"})
    return article


def get_articles(page_id):
    _ = articles_sorted.clone()
    return _[page_id*10: min(page_id*10+10, articles_sorted.count())]


def get_articles_recently():
    return articles.find({"type": "article"}).sort('order', pymongo.DESCENDING)[:8]


def get_articles_single_user(username):
    return articles.find({'username': username, 'type': 'article'}).sort('order', pymongo.DESCENDING)


def del_articles_by_orders(orders):
    for order in orders:
        articles.remove({"order": order})


# for forum
def add_post(title, lz, content, time_post, plate, username):
    try:
        order = posts.find({'type': 'post'}).count()
        posts.insert_one({'order': order, 'type': 'post', 'title': title, 'lz': lz, 'content': content, 'time_post': time_post, 'plate': plate, 'username': username})
        return order
    except MemoryError:
        raise MemoryError


def add_comment_for_post(cz, content, username, time_comment, order):
    corder = posts.find({'order': order, 'type': 'comment'}).count() + 1
    posts.insert_one({'order': order, 'corder': corder, 'type': 'comment', 'cz': cz, 'content': content, 'username': username, 'time_comment': time_comment})


def get_post(order):
    return posts.find_one({'type': 'post', 'order': order})


def get_posts_by_plate(plate):
    return posts.find({'plate': plate}).sort('order', pymongo.DESCENDING)


def get_posts_recently():
    return posts.find({'type': 'post'}).sort('order', pymongo.DESCENDING)[:8]


# for search
def search_by_target(target):
    us = users.find({"nickname": {"$regex": r"(.)*"+target+r"(.)*"}})
    pos = posts.find({"title": {"$regex": r"(.)*"+target+r"(.)*"}})
    cods = codes.find({"poster": {"$regex": r"(.)*"+target+r"(.)*"}})
    arts = articles.find({"title": {"$regex": r"(.)*"+target+r"(.)*"}})
    return us, pos, cods, arts


def search_by_username(username):
    pos = posts.find({'username': username, 'type': 'post'})
    arts = articles.find({'username': username, 'type': 'article'})
    return pos, arts
