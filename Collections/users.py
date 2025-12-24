from db import users
from db import ConnectionFailure
from db import e

def getpass(username):
    try:
        x = users.find_one({"username":username})
        if x == None:
            return None
        return x["password"]
    except ConnectionFailure:
        e() 
