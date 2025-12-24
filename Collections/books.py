from db import books
from db import ConnectionFailure
from db import e

def i(x):
    try:
        x = int(x)
        if x < 0:
            raise
        return x
    except:
        raise ValueError("Total count and available count should be non-negative integer")

def addbook(title, author, category, total_count, available_count):
    #relation of total and available should be checked
    try:
        ltitle = title.lower()
        total_count = i(total_count)
        available_count = i(available_count)
        if total_count == 0:
            raise ValueError("Total count should be postive")
        if books.find_one({"ltitle":ltitle, "author":{"$regex":author + '$', "$options":"i"}}) != None:
            raise ValueError("This book is alredy in libraray")
        books.insert_one({"ltitle":ltitle, "title":title, "author":author, "category":category, "total_count":total_count, "available_count":available_count})
        return total_count
    except ConnectionFailure:
        e()