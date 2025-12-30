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
        raise ValueError("Duration should be a postive integer")

def o(x):
    try:
        return ObjectId(x)
    except:
        raise ValueError("_id is invalid")

def requestloan(username, _id, duration):
    try:
        duration = i(duration)
        if requests.find_one({"username":username, "book id": _id, "status":"pending", "type":"loan"}) != None:
            raise Exception("You have alredy requeted this")
        requests.insert_one({"username":username, "book id":_id, "request date":datetime.now().replace(microsecond=0), "duration":duration, "status":"pending", "type":"loan"})
    except ConnectionFailure:
        e()

def exist(username, _id):
    try:
        if requests.find_one({"username":username, "book id":_id, "status":"pending"}, {"_id":0, "username":0}) != None:
            raise Exception("You alredy have a pending request on this book")
    except ConnectionFailure:
        e()
def request_renew(username, _id, duration):
    try:
        duration = i(duration)
        if requests.find_one({"username":username, "book id": _id, "status":"pending", "type":"renew"}) != None:
            raise Exception("You have alredy requeted this")
        requests.insert_one({"username":username, "book id":_id, "request date":datetime.now().replace(microsecond=0), "duration":duration, "status":"pending", "type":"renew"})
    except ConnectionFailure:
        e()

def request_return(username, _id):
    try:
        if requests.find_one({"username":username, "book id": _id, "status":"pending", "type":"return"}) != None:
            raise Exception("You have alredy requeted this")
        requests.insert_one({"username":username, "book id":_id, "request date":datetime.now().replace(microsecond=0), "status":"pending", "type":"return"})
    except ConnectionFailure:
        e()

def myrequests(username):
    try:
        return list(requests.find({"username": username}, {"_id": 0, "username": 0}))
    except ConnectionFailure:
        e()

def all_requests(username, status):
    try:
        status = status.lower()
        if status != "all":
            return requests.find({"username":{"$regex":username}, "status":status})
        return requests.find({"username":{"$regex":username}})
    except ConnectionFailure:
        e()
    
def get_request(_id):
    try:
        _id = o(_id)
        x = requests.find_one({"_id":_id})
        if x == None:
            raise ValueError("_id is not valid")
        return x
    except ConnectionFailure:
        e()

def change_status(_id, status):
    try:
        _id = o(_id)
        requests.update_one({"_id":_id}, {"$set":{"status":status}})
    except ConnectionFailure:
        e()

def del_request(book_id):
    try:
        requests.delete_many({"book id":book_id})
    except ConnectionFailure:
        e()
