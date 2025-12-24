from db import users
from db import ConnectionFailure
from db import e

#are CRU funcion returning something?

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
        if users.find_one({"username":username}) != None:
            raise ValueError("Username alredy taken")
        users.insert_one({"username":username, "password":password, "name":name, "role":role})
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