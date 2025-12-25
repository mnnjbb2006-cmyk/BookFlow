import db
from services import loans
from services import requests
from Collections import books
from Collections import users

def clear():
    print("\033[2J\033[H", end="")

def table(rows, col):
    s = ""
    if not rows:
        print("No data.")
        return s
    columns = list(map(str.lower, col))
    widths = {c: max(len(c), max(len(str(r.get(c, ""))) for r in rows)) for c in columns}
    header = " | ".join(c.ljust(widths[c.lower()]) for c in col)
    sep = "-+-".join("-" * widths[c] for c in columns)
    s = header + '\n'
    s += sep + '\n'
    for r in rows:
        s += (" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in columns)) + '\n'
    return '\n' + s

def r(prompt):
    x = input(prompt).strip()
    for c in x:
        if c == '$':
            raise ValueError("Input can not contain $")
    return x

def p(prompt="", options=[]):
    global log
    while(True):
        clear()
        print("\n" + prompt + log)
        log = ""
        x = 1
        for option in options:
            print(f"{x})", option)
            x += 1
        print("0) Exit")
        try:
            choice = int(r("> "))
            if choice < 0 or choice > x:
                raise
            if choice == 0:
                exit()
            return choice
        except SystemExit:
            raise
        except:
            log = "\nYou should enter a number from the below list"

def Admin(name, username):
    global log
    while(True):
        try:
            choice = p(f"Welcome {name} (Admin)", ["List Users", "Add User", "Remove User", "Disable/Enable user", "Find books", "Add books", "Edit books", "Requests", "Logout"])
            if choice == 9:
                return
            elif choice == 1:
                log = table(users.getusers(), ["Username", "Name", "Role", "Status"])
            elif choice == 2:
                l = ["Admin", "Librarian", "User"]
                choice = p("Select role:", l)
                u = users.adduser(r("Username: "), r("Password: "), r("Full name: "), l[choice - 1])
                log = f"\nSuccessfully created user {u}"
            elif choice == 3:
                u = r("Username: ")
                if u == username:
                    raise ValueError("You can not delete yourself")
                users.deluser(u)
                log = f"\nSuccessfully {u} was deleted"
            elif choice == 4:
                choice = p("", ["Enable", "Disable"])
                if choice == 2:
                    u = r("Username: ")
                    if u == username:
                        raise ValueError("You can not disable yourself")
                    users.disable(u)
                    log = f"\nSuccessfully disabled {u}"
                else:
                    u = r("Username: ")
                    users.enable(u)
                    log = f"\nSuccessfully enabled {u}"
            elif choice == 5:
                log = table(books.findbooks(r("Title (leave emtpy to not consider): "), r("Authore (leave emtpy to not consider): "), r("Categorye (leave emtpy to not consider): "), r("Min total counte (leave emtpy to not consider): "), r("Min available counte (leave emtpy to not consider): "), r("Max total counte (leave emtpy to not consider): "), r("Max available counte (leave emtpy to not consider): ")),
                ["_id", "Title", "Author", "Total count", "Available count"])
            elif choice == 6:
                log = f"\nSuccessfully addedd {books.addbook(r("Title: "), r("Author: "), r("Category: "), r("Total count: "), r("Available count: "))} books to library"
            elif choice == 7:
                _id = r("_id: ")
                x = books.i(r("New total count (enter 0 to delete): "))
                if x == 0:
                    books.delbook(_id)
                    log = f"\nSuccessfully the books were deleted"
                else:
                    books.editbook(_id, r("New Title (leave empty to not change): "), r("New author (leave empty to not change): "), r("New category (leave empty to not change): "), x, r("New available value: (leave empty to not change)"))
                    log = f"\nData edited successfully"
            elif choice == 8:
                choice = p("", ["List Requests", "Accept request", "Reject request"])
                if choice == 1:
                    uname = r("Username (leave empty to not consider): ")
                    x = ["All", "Accepted", "Rejected", "Pending"]
                    status = p("State:", x)
                    status = x[status - 1]
                    l = [(books.findbooks(_id=x['book id']) | x) for x in requests.all_requests(uname, status)]
                    log = table(l, ["Username", "Title", "Author", "Type", "Status", "Request date", "Duration", "_id"])
                elif choice == 2:
                    request = requests.get_request(r("Enter request _id: "))
                    if request["status"] != "pending":
                        raise ValueError("This request is not in pending status")
                    if request.get("type") == "loan":
                        book = books.findbooks(_id=request["book id"])
                        if book["available count"] == 0:
                            raise Exception("The book is currently unavailable")
                        books.editbook(request["book id"], available_count=book["available count"] - 1) 
                        loans.add_loan(request["username"], request["book id"], request["duration"])
                        requests.change_status(request["_id"], "accepted")
                        log = "\nLoan was successful"
                    elif request["type"] == "renew":
                        loans.del_loan(request["username"], request["book id"])
                        loans.add_loan(request["username"], request["book id"], request["duration"])
                        requests.change_status(request["_id"], "accepted")
                        log = "\nRenew was successful"
                    else:
                        loans.del_loan(request["username"], request["book id"])
                        requests.change_status(request["_id"], "accepted")
                        books.editbook(request["book id"], available_count=book["available count"] + 1) 
                        log = "\nReturn was successful"
                elif choice == 3:
                    request = requests.get_request(r("Enter request _id: "))
                    requests.change_status(request["_id"], "rejected")
                    log = "\Rejection was successful"
        except SystemExit:
            raise
        except Exception as e:
            log = f"\nError: {e}"

def Librarian(name, username):
    global log
    while(True):
        try:
            choice = p(f"Welcome {name} (Librarian)", ["Find books", "Add books", "Edit books", "Requests", "Logout"])
            if choice == 5:
                return
            elif choice == 1:
                log = table(books.findbooks(r("Title (leave emtpy to not consider): "), r("Authore (leave emtpy to not consider): "), r("Categorye (leave emtpy to not consider): "), r("Min total counte (leave emtpy to not consider): "), r("Min available counte (leave emtpy to not consider): "), r("Max total counte (leave emtpy to not consider): "), r("Max available counte (leave emtpy to not consider): ")),
                ["_id", "Title", "Author", "Total count", "Available count"])
            elif choice == 2:
                log = f"\nSuccessfully addedd {books.addbook(r("Title: "), r("Author: "), r("Category: "), r("Total count: "), r("Available count: "))} books to library"
            elif choice == 3:
                _id = r("_id: ")
                x = books.i(r("New total count (enter 0 to delete): "))
                if x == 0:
                    books.delbook(_id)
                    log = f"\nSuccessfully the books were deleted"
                else:
                    books.editbook(_id, r("New Title (leave empty to not change): "), r("New author (leave empty to not change): "), r("New category (leave empty to not change): "), x, r("New available value: (leave empty to not change)"))
                    log = f"\nData edited successfully"
            elif choice == 4:
                choice = p("", ["List Requests", "Accept request", "Reject request"])
                if choice == 1:
                    uname = r("Username (leave empty to not consider): ")
                    x = ["All", "Accepted", "Rejected", "Pending"]
                    status = p("State:", x)
                    status = x[status - 1]
                    l = [(books.findbooks(_id=x['book id']) | x) for x in requests.all_requests(uname, status)]
                    log = table(l, ["Username", "Title", "Author", "Type", "Status", "Request date", "Duration", "_id"])
                elif choice == 5:
                    request = requests.get_request(r("Enter request _id: "))
                    if request["status"] != "pending":
                        raise ValueError("This request is not in pending status")
                    if request.get("type") == "loan":
                        book = books.findbooks(_id=request["book id"])
                        if book["available count"] == 0:
                            raise Exception("The book is currently unavailable")
                        books.editbook(request["book id"], available_count=book["available count"] - 1) 
                        loans.add_loan(request["username"], request["book id"], request["duration"])
                        requests.change_status(request["_id"], "accepted")
                        log = "\nLoan was successful"
                    elif request["type"] == "renew":
                        loans.del_loan(request["username"], request["book id"])
                        loans.add_loan(request["username"], request["book id"], request["duration"])
                        requests.change_status(request["_id"], "accepted")
                        log = "\Renew was successful"
                    else:
                        loans.del_loan(request["username"], request["book id"])
                        requests.change_status(request["_id"], "accepted")
                        books.editbook(request["book id"], available_count=book["available count"] + 1) 
                        log = "\nReturn was successful"
                elif choice == 3:
                    request = requests.get_request(r("Enter request _id: "))
                    requests.change_status(request["_id"], "rejected")
                    log = "\Rejection was successful"
        except SystemExit:
            raise
        except Exception as e:
            log = f"\nError: {e}"

def User(name, username):
    global log
    while(True):
        try:
            choice = p(f"Welcome {name} (User)", ["Find books", "My loans", "Requests", "Logout"])
            if choice == 4:
                return
            elif choice == 1:
                log = table(books.findbooks(r("Title (leave emtpy to not consider): "), r("Authore (leave emtpy to not consider): "), r("Categorye (leave emtpy to not consider): "), r("Min total counte (leave emtpy to not consider): "), r("Min available counte (leave emtpy to not consider): "), r("Max total counte (leave emtpy to not consider): "), r("Max available counte (leave emtpy to not consider): ")),
                ["_id", "Title", "Author", "Total count", "Available count"])
            elif choice == 2:
                loan = loans.my_loans(username)
                complete = [x | books.findbooks(_id=x["book id"]) for x in loan]
                log = table(complete, ["Title", "Author", "Accepted date", "Return Date", "Book id"])
            elif choice == 3:
                #should check my loans
                choice = p("", ["My requests", "Request loan", "Request renew", "Request return"])
                if choice == 1:
                    l = [(books.findbooks(_id=x['book id']) | x) for x in requests.myrequests(username)]
                    log = table(l, ["Title", "Author", "Type", "Status", "Request date", "Duration"])
                elif choice == 2:
                    _id = r("_id of book: ")
                    x = books.findbooks(_id=_id)
                    if x == None:
                        raise ValueError("The _id is invalid")
                    if x['available count'] == 0:
                        raise ValueError("The book is currently unavailable")
                    if loans.check_to_loan(username, _id) == True:
                        raise ValueError("You alredy have this book")
                    requests.requestloan(username, _id, r("Duration: "))
                    log = "\nRequest sent successfully"
                elif choice == 3:
                    _id = r("_id of book: ")
                    if books.findbooks(_id=_id) == None:
                        raise ValueError("The _id is invalid")
                    if loans.check_to_loan(username, _id) == False:
                        raise ValueError("You do not have this book")
                    requests.request_renew(username, _id, r("Duration: "))
                    log = "\nRequest sent successfully"
                elif choice == 4:
                    _id = r("_id of book: ")
                    if books.findbooks(_id=_id) == None:
                        raise ValueError("The _id is invalid")
                    if loans.check_to_loan(username, _id) == False:
                        raise ValueError("You do not have this book")
                    requests.request_return(username, _id)
                    log = "\nRequest sent successfully"
        except SystemExit:
            raise
        except Exception as e:
            log = f"\nError: {e}"

log = ""
while(True):
    p("Library Manager:", ['Login'])
    try:
        username = r("Username: ")
        password = r("Password: ")
        x = users.getuser(username)
        if  x["password"] == password:
            if x["status"] == "disabled":
                raise Exception("This user is disabled")
            eval(x['role'] + """(x["name"], username)""")
        else:
            raise ValueError("This user does not exist")
    except SystemExit:
        raise
    except Exception as e:
        log = f"\nError: {e}"