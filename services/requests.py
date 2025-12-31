from db import requests
from db import e
from db import ConnectionFailure
from bson import ObjectId
from datetime import datetime

def i(x):
    try:
        x = int(x)
        if x <= 0:
            raise
        return x
    except:
        raise ValueError("Duration should be a positive integer")

def o(x):
    try:
        return ObjectId(x)
    except:
        raise ValueError("_id is invalid")

def requestloan(username, _id, duration):
    duration = i(duration)
    if requests.find_one({"username":username, "book id": _id, "status":"pending", "type":"loan"}) != None:
        raise Exception("You have already requested this")
    requests.insert_one({"username":username, "book id":_id, "request date":datetime.now().replace(microsecond=0), "duration":duration, "status":"pending", "type":"loan"})

def exist(username, _id):
    if requests.find_one({"username":username, "book id":_id, "status":"pending"}, {"_id":0, "username":0}) != None:
        raise Exception("You already have a pending request on this book")
def request_renew(username, _id, duration):
    duration = i(duration)
    if requests.find_one({"username":username, "book id": _id, "status":"pending", "type":"renew"}) != None:
        raise Exception("You have already requested this")
    requests.insert_one({"username":username, "book id":_id, "request date":datetime.now().replace(microsecond=0), "duration":duration, "status":"pending", "type":"renew"})

def request_return(username, _id):
    if requests.find_one({"username":username, "book id": _id, "status":"pending", "type":"return"}) != None:
        raise Exception("You have already requested this")
    requests.insert_one({"username":username, "book id":_id, "request date":datetime.now().replace(microsecond=0), "status":"pending", "type":"return"})

def myrequests(username):
    return list(requests.find({"username": username}, {"_id": 0, "username": 0}))

def all_requests(username, status):
    status = status.lower()
    if status != "all":
        return requests.find({"username":{"$regex":username}, "status":status})
    return requests.find({"username":{"$regex":username}})
    
def get_request(_id):
    _id = o(_id)
    x = requests.find_one({"_id":_id})
    if x == None:
        raise ValueError("_id is not valid")
    return x

def change_status(_id, status):
    _id = o(_id)
    requests.update_one({"_id":_id}, {"$set":{"status":status}})

def del_request(book_id):
    requests.delete_many({"book id":book_id})

def del_request_user(username):
    requests.delete_many({"username":username})