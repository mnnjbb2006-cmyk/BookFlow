from db import loans
from db import e
from db import ConnectionFailure
from bson import ObjectId
from datetime import datetime, timedelta

def my_loans(username):
    return list(loans.find({"username": username}, {"_id": 0, "username": 0}))

def add_loan(username, book_id, duration):
    x = datetime.now().replace(microsecond=0)
    loans.insert_one({'username':username, 'book id' : book_id, "accepted date":x, "return date":x + timedelta(duration)})

def check_to_loan(username, book_id):
    if loans.find_one({'username':username, 'book id' : book_id}) != None:
        return True
    return False

def del_loan(username, book_id):
    loans.delete_one({"username": username, "book id": book_id})