# -*- coding: utf-8 -*-
import pymongo


conn = pymongo.MongoClient('localhost', 27017)
db = conn.demoblog

users = db.users
codes = db.codes
articles = db.articles


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
def add_article(title, author, content, time_post):
    try:
        order = articles.find().count()
        articles.insert_one({'title': title, 'author': author, 'content': content, 'order': order, 'time_post': time_post})
        return order
    except:
        raise MemoryError
# TODO: refresh the articles(sorted) after one add.

def get_article(article_id):
    article = articles.find_one({'order': article_id})
    return article['title'], article['author'], article['content']


def get_articles():
    pass
# TODO: get the articles from add_article() and return the special articles.
