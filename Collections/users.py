from db import users
from db import ConnectionFailure
from db import e

"""Helpers for the `users` collection (validation wrappers)."""

def getusers():
    return list(users.find({}, {"_id": 0}))

def getuser(username):
    # Return a user document or raise ValueError if not found.
    x = users.find_one({"username": username})
    if x == None:
        raise ValueError("This user does not exist")
    return x

def adduser(username, password, name, role):
    # Create a new user. Raises on invalid input or existing username.
    if username == "" or password == "" or name == "":
        raise ValueError("Username, password and name must not be empty")
    if users.find_one({"username": username}) != None:
        raise ValueError("Username already taken")
    users.insert_one({"username": username, "password": password, "name": name, "role": role, "status": "enabled"})
    return username

def deluser(username):
    x = users.delete_one({"username":username}).deleted_count
    if x == 0:
        raise ValueError("This user does not exist")

def disable(username):
    x = users.update_one({"username":username}, {"$set":{"status":"disabled"}})
    if x.matched_count == 0:
        raise ValueError("This user does not exist")
    if x.modified_count == 0:
        raise ValueError("This user was already disabled")

def enable(username):
    x = users.update_one({"username":username}, {"$set":{"status":"enabled"}})
    if x.matched_count == 0:
        raise ValueError("This user does not exist")
    if x.modified_count == 0:
        raise ValueError("This user was already enabled")