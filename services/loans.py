from db import loans
from db import e
from db import ConnectionFailure
from bson import ObjectId
from datetime import datetime, timedelta

"""Loan helpers: manage records in the `loans` collection."""

def my_loans(username):
    # Return a list of loans for the given username (omit _id/username).
    return list(loans.find({"username": username}, {"_id": 0, "username": 0}))


def add_loan(username, book_id, duration):
    # Insert a loan record; duration is in days.
    x = datetime.now().replace(microsecond=0)
    loans.insert_one({'username': username, 'book id': book_id, "accepted date": x, "return date": x + timedelta(duration)})


def check_to_loan(username, book_id):
    # Return True if the user already has a loan for the given book.
    if loans.find_one({'username': username, 'book id': book_id}) != None:
        return True
    return False


def del_loan(username, book_id):
    # Delete a single loan record for a user/book pair.
    loans.delete_one({"username": username, "book id": book_id})