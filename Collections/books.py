from db import books
from db import ConnectionFailure
from bson import ObjectId

"""Helpers for the `books` collection (validation and CRUD helpers)."""

def i(x):
    # Convert to int and ensure non-negative; raise ValueError on fail.
    try:
        x = int(x)
        if x < 0:
            raise
        return x
    except:
        raise ValueError("Total count should be a non-negative integer")

def o(x):
    # Convert a string to bson.ObjectId; raise ValueError on failure.
    try:
        return ObjectId(x)
    except:
        raise ValueError("_id is invalid")

def addbook(title, author, category, total_count):
    # Add a new book to the collection; validate inputs first.
    if title == "" or author == "" or total_count == "":
        raise ValueError("Title, author and total_count must not be empty")
    ltitle = title.lower()
    total_count = i(total_count)
    if total_count == 0:
        raise ValueError("Total count should be positive")
    if books.find_one({"ltitle":ltitle, "author":{"$regex":author + '$', "$options":"i"}}) != None:
        raise ValueError("This book already exists in the library")
    books.insert_one({"ltitle":ltitle, "title":title, "author":author, "category":category, "total count":total_count, "available count":total_count, "loans":0, "loaned":0})
    return total_count

def findbooks(title="", author="", category="", min_total="", min_available="", max_total="", max_available="", _id=""):
    # Find books by filters. If `_id` provided return single book.
    if _id != "":
        #_id = o(_id)
        x = books.find_one({"_id": _id})
        if x == None:
            raise ValueError("This book does not exist")
        return x
    query = {}

    if title != "":
        query["ltitle"] = {"$regex": title.lower()}

    if author != "":
        query["author"] = {"$regex": author, "$options": "i"}

    if category != "":
        query["category"] = {"$regex": category, "$options": "i"}

    total_range = {}
    if min_total != "":
        total_range["$gte"] = i(min_total)
    if max_total != "":
        total_range["$lte"] = i(max_total)
    if total_range:
        query["total count"] = total_range

    avail_range = {}
    if min_available != "":
        avail_range["$gte"] = i(min_available)
    if max_available != "":
        avail_range["$lte"] = i(max_available)
    if avail_range:
        query["available count"] = avail_range

    return list(books.find(query))


def most_loaned(limit):
    # Return a list of up to `limit` books sorted by the 'loaned' field descending.
    if limit == 0:
        raise ValueError("Limit should be a positive integer")
    return list(books.find({}).sort("loaned", -1).limit(limit))

def delbook(_id):
    # Delete a book; prevent deletion when active loans exist.
    _id = o(_id)
    x = books.find_one({"_id": _id})
    if x == None:
        raise ValueError("_id is invalid")
    loans = x["loans"]
    if loans != 0:
        raise ValueError(f"This book is currently loaned by {loans} user(s); total count cannot be less than {loans}.")
    books.delete_one({"_id": _id})

def editbook(_id, title="", author="", category="", total_count="", available_count="", loans_num="", loaned="", auto=True):
    # Edit book metadata. When auto=False, available_count = total_count - loans_num.
    _id = o(_id)
    x = books.find_one({"_id": _id})
    if x == None:
        raise ValueError("This book does not exist")
    query = {}
    if title != "":
        query["title"] = title
    if author != "":
        query["author"] = author
    if category != "":
        query["category"] = category
    if total_count != "":
        query["total count"] = i(total_count)
    if loaned != "":
        query["loaned"] = i(loaned)
    if loans_num != "":
        query["loans"] = i(loans_num)
    if auto == False:
        if total_count == 0:
            raise ValueError("Totatl count should be positive")
        if total_count < loans_num:
            raise ValueError(f"This book is currently loaned by {loans_num} user(s); total count cannot be less than {loans_num}.")
        available_count = total_count - loans_num
    ltitle = title.lower()
    x = books.find_one({"ltitle":ltitle, "author":{"$regex":author + "$", "$options":"i"}})
    if x != None and x['_id'] != _id:
        raise ValueError("Another book with the same title and author already exists")
    x = books.update_one({"_id":_id}, {"$set":query}).modified_count
    if x == 0:
        raise Exception("Nothing has been changed")