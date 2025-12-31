from db import books
from db import ConnectionFailure
from bson import ObjectId

def i(x):
    try:
        x = int(x)
        if x < 0:
            raise
        return x
    except:
        raise ValueError("Total count should be non-negeative integer")

def o(x):
    try:
        return ObjectId(x)
    except:
        raise ValueError("_id is invalid")

def addbook(title, author, category, total_count):
    if title == "" or author == "" or total_count == "":
        raise ValueError("Inputs can not be empty")
    ltitle = title.lower()
    total_count = i(total_count)
    if total_count == 0:
        raise ValueError("Total count should be postive")
    if books.find_one({"ltitle":ltitle, "author":{"$regex":author + '$', "$options":"i"}}) != None:
        raise ValueError("This book is alredy in libraray")
    books.insert_one({"ltitle":ltitle, "title":title, "author":author, "category":category, "total count":total_count, "available count":total_count, "loans":0, "loaned":0})
    return total_count

def findbooks(title="", author="", category="", min_total="", min_available="", max_total="", max_available="", _id=""):
    if _id != "":
        _id = o(_id) 
        x = books.find_one({"_id":_id})
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

def delbook(_id):
    _id = o(_id)
    x = books.find_one({"_id": _id})
    if x == None:
        raise ValueError("_id is invalid")
    loans = x["loans"]
    if loans != 0:
        raise ValueError(f"This book is currnetly loaned by {loans} of useres so total count cant be less than {loans}")
    books.delete_one({"_id":_id})

def editbook(_id, title="", author="", category="", total_count="", available_count="", loans_num="", loaned="", auto=True):
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
    if loaned == "":
        loaned = x["loaned"]
    if loans_num == "":
        loans_num = x["loans"]
    if auto == False:
        if total_count < loans_num:
            raise ValueError(f"This book is currnetly loaned by {loans_num} of useres so total count cant be less than {loans_num}")
        available_count = total_count - loans_num
    ltitle = title.lower()
    x = books.find_one({"ltitle":ltitle, "author":{"$regex":author + "$", "$options":"i"}})
    if x != None and x['_id'] != _id:
        raise ValueError("There exist another book with same title and author")
    x = books.update_one({"_id":_id}, {"$set":{"ltitle":ltitle, "title":title, "author":author, "category":category, "total count":total_count, "available count":available_count, "loans":loans_num, "loaned":loaned}}).modified_count
    if x == 0:
        raise Exception("Nothing has been changed")