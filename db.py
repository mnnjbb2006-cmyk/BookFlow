from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def e():
        print("Cannot connect to the database; make sure MongoDB is running on the default port.")
        try:
            client.close()
        except Exception:
            pass
        exit(1)

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
loans.create_index("username")

if users.find_one({}) == None:
    users.insert_one({"username":"admin", "password":"admin", "name":"admin", "role":"Admin", "status":"enabled"})