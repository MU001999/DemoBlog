# -*- coding: utf-8 -*-

import pymongo
import bcrypt
from blog.common import *


conn = pymongo.MongoClient(get_config('mongodb', 'host'),
                           int(get_config('mongodb', 'port')),
                           authMechanism=get_config('mongodb', 'authMechanism'))
db = conn.demoblog
db.authenticate(get_config('mongodb', 'username'),
                get_config('mongodb', 'password'))

users = db.users
codes = db.codes
articles = db.articles
posts = db.posts

articles_sorted = articles.find({"type": "article"}).sort("order", pymongo.DESCENDING)


# common
class LinkDbError(Exception):
    def __init__(self, arg):
        self.args = arg


def get_comments(order, col):
    return eval(col).find({'type': 'comment', 'order': order}).sort('corder')


# for users
def check_password(password, hashed):
    password = to_str(password)
    hashed = to_str(hashed)
    return bcrypt.hashpw(password, hashed) == hashed


def check(username, password):
    try:
        if users.find_one({"username": username}):
            user = users.find_one({"username": username})
            hashed = user['password']
            if check_password(password, hashed):
                return user['nickname'], True
            else:
                return "password", False
        else:
            return "username", False
    except LinkDbError:
        raise LinkDbError("error at check() in link2db")


def check_exist(username):
    if users.find_one({"username": username}):
        return True
    return False


def add_user(username, password, nickname, email_addr):
    try:
        password = to_str(password)
        password = bcrypt.hashpw(password, bcrypt.gensalt(8))
        password = to_unicode(password)
        avatar_path = avatar_gen(username)
        users.insert_one({'username': username,
                          'password': password,
                          'nickname': nickname,
                          'avatar': avatar_path,
                          'sign': "热爱学习",
                          'email_addr': email_addr})
    except LinkDbError:
        raise LinkDbError("error at add_user() in link2db")
    else:
        return True


def update_user(username, u2n, info):
    if info == "pwd":
        u2n = to_str(u2n)
        u2n = bcrypt.hashpw(u2n, bcrypt.gensalt(8))
        u2n = to_unicode(u2n)
        users.update({"username": username},
                     {"$set": {"password": u2n}})
    elif info == "info":
        global articles_sorted
        users.update({"username": username},
                     {"$set": {"nickname": u2n[0],
                               "sign": u2n[1],
                               "email_addr": u2n[2],
                               "github_username": u2n[3]}}, multi=True, upsert=True)
        articles.update({"username": username},
                        {"$set": {"author": u2n[0]}}, multi=True, upsert=True)
        posts.update({"username": username},
                     {"$set": {"lz": u2n[0]}}, multi=True)
        articles_sorted = articles.find({"type": "article"}).sort("order", pymongo.DESCENDING)
    elif info == "avatar":
        users.update({"username": username},
                     {"$set": {"avatar": u2n}}, upsert=True)


def get_user(username):
    return users.find_one({'username': username})


# for codes
def add_code(poster, syntax, content):
    try:
        order = codes.find().count()
        codes.insert_one({'poster': poster,
                          'syntax': syntax,
                          'content': content,
                          'order': order})
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
        order = (articles_sorted[0]['order'] or 0) + 1
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
                    {"$set": {"title": title,
                              "content": content,
                              "labels": labels,
                              "completed": completed}})
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
        posts.insert_one({'order': order,
                          'type': 'post',
                          'title': title,
                          'lz': lz,
                          'content': content,
                          'time_post': time_post,
                          'plate': plate,
                          'username': username})
        return order
    except LinkDbError:
        raise LinkDbError("error at add_post() in link2db")


def add_comment_for_post(cz, content, username, time_comment, order):
    corder = posts.find({'order': order, 'type': 'comment'}).count() + 1
    posts.insert_one({'order': order,
                      'corder': corder,
                      'type': 'comment',
                      'cz': cz,
                      'content': content,
                      'username': username,
                      'time_comment': time_comment})


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
