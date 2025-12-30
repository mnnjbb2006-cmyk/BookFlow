from db import loans
from db import e
from db import ConnectionFailure
from bson import ObjectId
from datetime import datetime, timedelta

def my_loans(username):
    try:
        return list(loans.find({"username": username}, {"_id": 0, "username": 0}))
    except ConnectionFailure:
        e()

def add_loan(username, book_id, duration):
    try:
        x = datetime.now().replace(microsecond=0)
        loans.insert_one({'username':username, 'book id' : book_id, "accepted date":x, "return date":x + timedelta(duration)})
    except ConnectionFailure:
        e()

def check_to_loan(username, book_id):
    try:
        if loans.find_one({'username':username, 'book id' : book_id}) != None:
            return True
        return False
    except ConnectionFailure:
        e()

def del_loan(username, book_id):
    try:
        loans.delete_one({"username": username, "book id": book_id})
    except ConnectionFailure:
        e()