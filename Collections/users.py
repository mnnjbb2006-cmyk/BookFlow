from db import users
from db import ConnectionFailure
from db import e
import hashlib

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
    # store hashed password (guard against invalid encoding inputs)
    try:
        b = password.encode('utf-8')
    except:
        # Friendly message for admin/user if their input cannot be encoded
        raise ValueError("Password must be valid UTF-8 text")
    hashed = hashlib.sha256(b).hexdigest()
    users.insert_one({"username": username, "password": hashed, "name": name, "role": role, "status": "enabled"})
    return username


def verify_password(username, password):
    """Return True if the provided password matches the stored hash."""
    x = users.find_one({"username": username})
    # ensure password can be encoded before hashing
    try:
        b = password.encode('utf-8')
    except:
        raise ValueError("Password must be valid UTF-8 text")

    if x is None or x.get("password") != hashlib.sha256(b).hexdigest():
        raise ValueError("This user does not exist")
    return x

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

if users.find_one({}) == None:
    # create default admin with hashed password
    admin_hashed = hashlib.sha256("admin".encode()).hexdigest()
    adduser("admin", "admin", "admin", "Admin")
    print("Default admin user created (username: admin, password: admin)")