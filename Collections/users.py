from db import users
from db import ConnectionFailure
from db import e

#are CRU funcion returning something?

def getusers():
    try:
        return users.find({}, {"_id":0}).to_list()
    except ConnectionFailure:
        e() 

def getuser(username):
    try:
        x = users.find_one({"username":username})
        if x == None:
            raise ValueError("This user does not exist")
        return x
    except ConnectionFailure:
        e() 

def adduser(username, password, name, role):
    try:
        if username == "" or password == "" or name == "":
            raise ValueError("Username or password or name can not be empty")
        if users.find_one({"username":username}) != None:
            raise ValueError("Username alredy taken")
        users.insert_one({"username":username, "password":password, "name":name, "role":role, "status":"enabled"})
        return username
    except ConnectionFailure:
        e() 

def deluser(username):
    try:
        x = users.delete_one({"username":username}).deleted_count
        if x == 0:
            raise ValueError("This user does not exist")
    except ConnectionFailure:
        e() 

def disable(username):
    try:
        x = users.update_one({"username":username}, {"$set":{"status":"disabled"}})
        if x.matched_count == 0:
            raise ValueError("This user does not exist")
        if x.modified_count == 0:
            raise ValueError("This user was alredy disabled")
    except ConnectionFailure:
        e() 

def enable(username):
    try:
        x = users.update_one({"username":username}, {"$set":{"status":"enabled"}})
        if x.matched_count == 0:
            raise ValueError("This user does not exist")
        if x.modified_count == 0:
            raise ValueError("This user was alredy enbled")
    except ConnectionFailure:
        e() 