from db import requests
from db import e
from db import ConnectionFailure
from bson import ObjectId
from datetime import datetime

"""Request helpers: create and query user requests."""


def i(x):
    """Parse and validate a positive integer duration (days)."""
    try:
        x = int(x)
        if x <= 0:
            raise
        return x
    except:
        raise ValueError("Duration should be a positive integer")


def o(x):
    """Convert a string to ObjectId."""
    try:
        return ObjectId(x)
    except:
        raise ValueError("_id is invalid")


def requestloan(username, _id, duration):
    """Create a loan request; ensure no duplicate pending one exists."""
    duration = i(duration)
    if requests.find_one({"username": username, "book id": _id, "status": "pending"}) != None:
        raise Exception("You already have a pending request on this book")
    requests.insert_one({"username": username, "book id": _id, "request date": datetime.now().replace(microsecond=0), "duration": duration, "status": "pending", "type": "loan"})


def exist(username, _id):
    """Raise if the user already has a pending request for the book."""
    if requests.find_one({"username": username, "book id": _id, "status": "pending"}, {"_id": 0, "username": 0}) != None:
        raise Exception("You already have a pending request on this book")


def request_renew(username, _id, duration):
    """Create a renew request."""
    duration = i(duration)
    if requests.find_one({"username": username, "book id": _id, "status": "pending"}) != None:
        raise Exception("You already have a pending request on this book")
    requests.insert_one({"username": username, "book id": _id, "request date": datetime.now().replace(microsecond=0), "duration": duration, "status": "pending", "type": "renew"})


def request_return(username, _id):
    """Create a return request."""
    if requests.find_one({"username": username, "book id": _id, "status": "pending"}) != None:
        raise Exception("You already have a pending request on this book")
    requests.insert_one({"username": username, "book id": _id, "request date": datetime.now().replace(microsecond=0), "status": "pending", "type": "return"})


def myrequests(username):
    """Return requests by username (omit username/_id)."""
    return list(requests.find({"username": username}, {"_id": 0, "username": 0}))


def all_requests(username, status):
    """Return cursor for requests filtered by username regex and status."""
    status = status.lower()
    if status != "all":
        return requests.find({"username": {"$regex": username}, "status": status})
    return requests.find({"username": {"$regex": username}})
    

def get_request(_id):
    """Return a single request document by ObjectId string."""
    _id = o(_id)
    x = requests.find_one({"_id": _id})
    if x == None:
        raise ValueError("_id is not valid")
    return x


def change_status(_id, status):
    """Set the status of a request (accepted/rejected)."""
    _id = o(_id)
    requests.update_one({"_id": _id}, {"$set": {"status": status}})


def del_request(book_id):
    """Delete all requests that reference a given book id."""
    requests.delete_many({"book id": book_id})


def del_request_user(username):
    """Delete all requests for a username (used when removing users)."""
    requests.delete_many({"username": username})

def del_book(_id):
    requests.delete_many({"book id": _id})