import pymongo


conn = pymongo.MongoClient('localhost', 27017)
db = conn.demoblog
col = db.users

def check(username, password):
    if col.find_one({"username": username, 'password': password}):
        return col.find_one({"username": username, 'password': password})['nickname']
    return None

def check_exist(username):
    if col.find_one({"username": username}):
        return True
    return False

def add_user(username, password, nickname):
    try:
        col.insert_one({'username': username, 'password': password, 'nickname': nickname})
        return True
    except:
        raise False