from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def e():
        print(f"Can not connect to database")
        client.close()
        exit()

try:
    client = MongoClient("mongodb://localhost/?directConnection=true", serverSelectionTimeoutMS=2000)
    client.admin.command("ping")
except:
    e()

db = client["lib"]
users = db["users"]
books = db["books"]
requests = db["request"]
loans = db["loans"]

users.create_index("username", unique=True)
books.create_index("ltitle")
requests.create_index("username")
loans.create_index("ltitle")

if users.find_one({}) == None:
    users.insert_one({"username":"admin", "password":"admin", "name":"admin", "role":"Admin", "status":"enabled"})