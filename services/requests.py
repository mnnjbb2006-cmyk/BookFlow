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

def myrequests(username):
    try:
        return requests.find({"username":username}, {"_id":0, "username":0}).to_list()
    except ConnectionFailure:
        e()

def requestrenew(username, _id, duration):
    try:
        duration = i(duration)
        if requests.find_one({"username":username, "book id": _id, "status":"pending", "type":"renew"}) != None:
            raise Exception("You have alredy requeted this")
        requests.insert_one({"username":username, "book id":_id, "request date":datetime.now().replace(microsecond=0), "duration":duration, "status":"pending", "type":"renew"})
    except ConnectionFailure:
        e()

def requestreturn(username, _id):
    try:
        duration = i(duration)
        if requests.find_one({"username":username, "book id": _id, "status":"pending", "type":"return"}) != None:
            raise Exception("You have alredy requeted this")
        requests.insert_one({"username":username, "book id":_id, "request date":datetime.now().replace(microsecond=0), "status":"pending", "type":"return"})
    except ConnectionFailure:
        e()

def myrequests(username):
    try:
        return requests.find({"username":username}, {"_id":0, "username":0}).to_list()
    except ConnectionFailure:
        e()