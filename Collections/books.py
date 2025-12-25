from db import books
from db import ConnectionFailure
from db import e
from bson import ObjectId

max_book = 0
for x in books.find({}).to_list():
    max_book = max(max_book, x["total count"], x["available count"])

def i(x):
    try:
        x = int(x)
        if x < 0:
            raise
        return x
    except:
        raise ValueError("Total count and available count should be non-negative integer")

def o(x):
    try:
        return ObjectId(x)
    except:
        raise ValueError("_id is invalid")

def addbook(title, author, category, total_count, available_count):
    #relation of total and available should be checked
    global max_book
    if title == "" or author == "" or total_count == "" or available_count == "":
        raise ValueError("Inputs can not be empty")
    try:
        ltitle = title.lower()
        total_count = i(total_count)
        available_count = i(available_count)
        if total_count == 0:
            raise ValueError("Total count should be postive")
        if books.find_one({"ltitle":ltitle, "author":{"$regex":author + '$', "$options":"i"}}) != None:
            raise ValueError("This book is alredy in libraray")
        books.insert_one({"ltitle":ltitle, "title":title, "author":author, "category":category, "total count":total_count, "available count":available_count})
        max_book += total_count
        return total_count
    except ConnectionFailure:
        e()

def findbooks(title, author, category, min_total, min_available, max_total, max_available):
    global max_book
    try:
        ltitle = title.lower()
        if max_total == "":
            max_total = max_book
        if max_available == "":
            max_available = max_book
        if min_total == "":
            min_total = 0
        if min_available == "":
            min_available = 0
        max_total = i(max_total)
        max_available = i(max_available)
        min_total = i(min_total)
        min_available = i(min_available)
        #return books.find({"ltitle":{"$regex":title, "$options":"i"}, "author":{"$regex":author, "$options":"i"}}).to_list()
        return books.find({"ltitle":{"$regex":title, "$options":"i"}, "author":{"$regex":author, "$options":"i"}, "category":{"$regex":category, "$options":"i"}, "total count":{"$lte":max_total, "$gte":min_total}, "available count":{"$lte":max_available, "$gte":min_available}}).to_list()
    except ConnectionFailure:
        e()

def delbook(_id):
    try:
        _id = o(_id)
        x = books.delete_one({"_id":_id}).deleted_count
        if x == 0:
            raise ValueError("This book does not exist")
    except ConnectionFailure:
        e()

def editbook(_id, title, author, category, total_count, available_count):
    try:
        _id = o(_id)
        x = books.find_one({"_id":_id})
        if x == None:
            raise ValueError("This book does not exist")
        if title == "":
            title = x["title"]
        if author == "":
            author = x["author"]
        if category == "":
            category = x["category"]
        if total_count == "":
            total_count = x["total count"]
        if available_count == "":
            available_count = x["available count"]
        available_count = i(available_count)
        ltitle = title.lower()
        x = books.find_one({"ltitle":ltitle, "author":{"$regex":author, "$options":"i"}})
        if x != None and x['_id'] != _id:
            raise ValueError("There exist another book with same title and author")
        x = books.update_one({"_id":_id}, {"$set":{"ltitle":ltitle, "title":title, "author":author, "category":category, "total count":total_count, "available count":available_count}}).modified_count
        if x == 0:
            raise Exception("Nothing has been changed")
    except ConnectionFailure:
        e()