import pymongo
"""
conn = pymongo.MongoClient('localhost', 27017)
db = conn.demoblog
col = db.users

def check_exist(userid):
    if col.find_one({"userid": userid}):
        return True
    return False
"""

def check_exist(userid):
    return True