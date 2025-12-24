from db import users
from db import ConnectionFailure
from db import e

def getuser(username):
    try:
        x = users.find_one({"username":username})
        if x == None:
            raise ValueError("This user does not exist")
        return x
    except ConnectionFailure:
        e() 
