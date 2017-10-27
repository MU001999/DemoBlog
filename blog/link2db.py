# -*- coding: utf-8 -*-
import pymongo


conn = pymongo.MongoClient('localhost', 27017)
db = conn.demoblog

users = db.users
codes = db.codes
articles = db.articles
posts = db.posts

articles_sorted = articles.find().sort("order")


# for users
def check(username, password):
    if users.find_one({"username": username, 'password': password}):
        return users.find_one({"username": username, 'password': password})['nickname']
    return None


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
        users.update({"username": username}, {"$set": {"nickname": u2n}})
        articles.update({"username": username}, {"$set": {"nickname": u2n}})
        articles_sorted = articles.find().sort("order")


# for codes
def add_code(poster, syntax, content):
    try:
        order = codes.find().count()
        codes.insert_one({'poster': poster, 'syntax': syntax, 'content': content, 'order': order})
        return order
    except:
        raise MemoryError


def get_code(order):
    code = codes.find_one({"order": order})
    return code['poster'], code['syntax'], code['content']


# for articles
def add_article(title, author, content, time_post, username):
    global articles_sorted
    try:
        order = articles.find().count()
        articles.insert_one({'title': title, 'author': author, 'content': content, 'order': order, 'time_post': time_post, 'username': username})
        articles_sorted = articles.find().sort("order")
        return order
    except:
        raise MemoryError


def get_article(article_id):
    article = articles.find_one({'order': article_id})
    return article['title'], article['author'], article['content'], article['time_post']


def get_articles(page_id):
    _ = articles_sorted.clone()
    return _[page_id*10: min(page_id*10+10, articles_sorted.count())]


def get_articles_single_user(username):
    return articles.find({'username': username}).sort('order')


def del_articles_by_orders(orders):
    for order in orders:
        articles.remove({"order": order})


# for forum
def add_post(title, lz, theme, content, time_post, plate, username):
    pass  # TODO: add post as {"title":title, "lz":lz...}


def add_comment():
    pass  # TODO: add comment and the comment has the same order with the post but have time_comment not time_post


def get_post(order):
    pass  # TODO: get the post as one floor and other floors as comments


def get_posts_recently():
    pass  # TODO: get 10 posts recently
