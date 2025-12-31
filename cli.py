import db
from db import ConnectionFailure
from services import loans
from services import requests
from Collections import books
from Collections import users

"""CLI for BookFlow — UI layer that calls Collections and services."""

def clear():
    print("\033[2J\033[H", end="")


def table(rows, cols):
    # Render rows (iterable of dicts) into a simple text table.
    if not rows:
        print("No data.")
        return ""

    columns = [c.lower() for c in cols]
    norm_rows = []
    for r in rows:
        norm_rows.append({str(k).lower(): v for k, v in r.items()})

    widths = {
        c: max(len(c), max(len(str(r.get(c, ""))) for r in norm_rows))
        for c in columns
    }

    sep = "-+-".join("-" * widths[c] for c in columns)
    header = " | ".join(c.ljust(widths[c]) for c in columns)

    out_lines = [header, sep]
    for r in norm_rows:
        out_lines.append(" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in columns))

    return "\n" + "\n".join(out_lines) + "\n"


def r(prompt):
    # Read a trimmed input line and reject '$' characters.
    x = input(prompt).strip()
    for c in x:
        if c == "$":
            raise ValueError("Input can not contain $")
    return x


log = ""


def p(prompt, options):
    global log

    # Show a numbered menu and return the selected index.
    while True:
        clear()
        print("\n" + prompt + log)
        log = ""

        for i, option in enumerate(options, start=1):
            print(f"{i})", option)
        print("0) Exit")

        try:
            choice = int(r("> "))
            if choice < 0 or choice > len(options):
                raise ValueError
            if choice == 0:
                raise SystemExit()
            return choice
        except SystemExit:
            raise
        except Exception:
            log = "\nYou should enter a number from the below list"


BOOK_COLS = ["_id", "Title", "Author", "Category", "Total count", "Available count", "Loans", "Loaned"]


def _book_find_flow():
    """Prompt for book search criteria and display results."""
    title = r("Title (leave empty to not consider): ")
    author = r("Author (leave empty to not consider): ")
    category = r("Category (leave empty to not consider): ")
    min_total = r("Min total count (leave empty to not consider): ")
    min_available = r("Min available count (leave empty to not consider): ")
    max_total = r("Max total count (leave empty to not consider): ")
    max_available = r("Max available count (leave empty to not consider): ")

    results = books.findbooks(
        title=title,
        author=author,
        category=category,
        min_total=min_total,
        min_available=min_available,
        max_total=max_total,
        max_available=max_available,
    )
    return table(results, BOOK_COLS)


def _book_add_flow():
    """Prompt and add a book; return a success message."""
    added = books.addbook(
        r("Title: "),
        r("Author: "),
        r("Category: "),
        r("Total count: "),
    )
    return f"\nSuccessfully added {added} book(s) to library"


def _book_edit_flow():
    """Edit a book or delete it when new total is 0."""
    _id = r("_id: ")
    new_total = books.i(r("New total count (enter 0 to delete): "))

    if new_total == 0:
        books.delbook(_id)
        requests.del_request(_id)
        return "\nSuccessfully the book was deleted"

    new_title = r("New title (leave empty to not change): ")
    new_author = r("New author (leave empty to not change): ")
    new_category = r("New category (leave empty to not change): ")

    books.editbook(
        _id,
        title=new_title,
        author=new_author,
        category=new_category,
        total_count=new_total,
        auto=False,
    )
    return "\nData edited successfully"


def _merge_book_into_request(req):
    """Attach book fields to a request dict for display."""
    info = books.findbooks(_id=req.get("book id", ""))
    return {**info, **req}


def _staff_requests_flow():
    """List/accept/reject requests (staff operations)."""
    sub = p("", ["List Requests", "Accept request", "Reject request"])
    if sub == 1:
        uname = r("Username (leave empty to not consider): ")
        states = ["All", "Accepted", "Rejected", "Pending"]
        status = states[p("State:", states) - 1]

        reqs = requests.all_requests(uname, status)
        merged = [_merge_book_into_request(x) for x in reqs]
        return table(merged, ["Username", "Title", "Author", "Type", "Status", "Request date", "Duration", "_id"])

    if sub == 2:
        req = requests.get_request(r("Enter request _id: "))
        if req.get("status") != "pending":
            raise ValueError("This request is not in pending status")

        rtype = req.get("type")
        book_id = req.get("book id")
        uname = req.get("username")

        if rtype == "loan":
            book = books.findbooks(_id=book_id)
            if book["available count"] == 0:
                raise Exception("The book is currently unavailable")
            books.editbook(
                book_id,
                available_count=book["available count"] - 1,
                loans_num=book["loans"] + 1,
                loaned=book["loaned"] + 1,
            )
            loans.add_loan(uname, book_id, req.get("duration"))
            requests.change_status(req.get("_id"), "accepted")
            return "\nLoan was successful"

        if rtype == "renew":
            loans.del_loan(uname, book_id)
            loans.add_loan(uname, book_id, req.get("duration"))
            requests.change_status(req.get("_id"), "accepted")
            return "\nRenew was successful"

        book = books.findbooks(_id=book_id)

        loans.del_loan(uname, book_id)
        books.editbook(
            book_id,
            available_count=book.get("available count", 0) + 1,
            loans_num=book.get("loans", 0) - 1,
        )
        requests.change_status(req.get("_id"), "accepted")
        return "\nReturn was successful"

    req = requests.get_request(r("Enter request _id: "))
    if req.get("status") != "pending":
        raise ValueError("This request is not in pending status")
    requests.change_status(req.get("_id"), "rejected")
    return "\nRejection was successful"


def Admin(name, username):
    global log
    # Admin menu (UI): calls Collections/services based on choice.
    while True:
        try:
            choice = p(
                f"Welcome {name} (Admin)",
                [
                    "List Users",
                    "Add user",
                    "Delete user",
                    "Enable/Disable user",
                    "Find books",
                    "Add books",
                    "Edit books",
                    "Requests",
                    "Logout",
                ],
            )

            if choice == 9:
                return
            elif choice == 1:
                log = table(users.getusers(), ["Username", "Name", "Role", "Status"])
            elif choice == 2:
                roles = ["Admin", "Librarian", "User"]
                role = roles[p("Select role:", roles) - 1]
                u = users.adduser(r("Username: "), r("Password: "), r("Full name: "), role)
                log = f"\nSuccessfully created user {u}"
            elif choice == 3:
                u = r("Username: ")
                if u == username:
                    raise ValueError("You can not delete yourself")
                if loans.my_loans(u) != []:
                    raise Exception("This user has active loans; cannot delete.")
                requests.del_request_user(u)
                users.deluser(u)
                log = f"\nSuccessfully {u} was deleted"
            elif choice == 4:
                action = p("", ["Enable", "Disable"])
                u = r("Username: ")
                if action == 2 and u == username:
                    raise ValueError("You can not disable yourself")
                (users.disable if action == 2 else users.enable)(u)
                log = f"\nSuccessfully {'disabled' if action == 2 else 'enabled'} {u}"
            elif choice == 5:
                log = _book_find_flow()
            elif choice == 6:
                log = _book_add_flow()
            elif choice == 7:
                log = _book_edit_flow()
            elif choice == 8:
                log = _staff_requests_flow()

        except ConnectionFailure:
            db.e()
        except Exception as e:
            log = f"\nError: {e}"


def Librarian(name, username):
    global log
    # Librarian menu (UI): book management and requests.
    while True:
        try:
            choice = p(
                f"Welcome {name} (Librarian)",
                ["Find books", "Add books", "Edit books", "Requests", "Logout"],
            )
            if choice == 5:
                return
            elif choice == 1:
                log = _book_find_flow()
            elif choice == 2:
                log = _book_add_flow()
            elif choice == 3:
                log = _book_edit_flow()
            elif choice == 4:
                log = _staff_requests_flow()

        except ConnectionFailure:
            db.e()
        except Exception as e:
            log = f"\nError: {e}"


def User(name, username):
    global log
    # User menu (UI): search books, view loans, create requests.
    while True:
        try:
            choice = p(f"Welcome {name} (User)", ["Find books", "My loans", "Requests", "Logout"])
            if choice == 4:
                return
            elif choice == 1:
                log = _book_find_flow()
            elif choice == 2:
                loan_rows = loans.my_loans(username)
                complete = []
                for x in loan_rows:
                    info = books.findbooks(_id=x.get("book id", ""))
                    complete.append({**info, **x})
                log = table(complete, BOOK_COLS)
            elif choice == 3:
                sub = p("", ["My Requests", "Request loan", "Request renew", "Request return", "Back"])
                if sub == 5:
                    continue

                if sub == 1:
                    reqs = requests.myrequests(username)
                    merged = [_merge_book_into_request(x) for x in reqs]
                    log = table(merged, ["Title", "Author", "Type", "Status", "Request date", "Duration", "Book id"])
                    continue

                _id = r("_id of book: ")
                if(_id == ""):
                    raise ValueError("_id can not be empty")
                b = books.findbooks(_id=_id)

                if sub == 2:
                    if b["available count"] == 0:
                        raise ValueError("The book is currently unavailable")
                    if loans.check_to_loan(username, _id):
                        raise ValueError("You already have this book")
                    requests.requestloan(username, _id, r("Duration: "))
                    log = "\nRequest sent successfully"

                elif sub == 3:
                    if not loans.check_to_loan(username, _id):
                        raise ValueError("You do not have this book")
                    requests.request_renew(username, _id, r("Duration: "))
                    log = "\nRequest sent successfully"

                elif sub == 4:
                    if not loans.check_to_loan(username, _id):
                        raise ValueError("You do not have this book")
                    requests.request_return(username, _id)
                    log = "\nRequest sent successfully"

        except ConnectionFailure:
            db.e()
        except Exception as e:
            log = f"\nError: {e}"


ROLE_HANDLERS = {
    "Admin": Admin,
    "Librarian": Librarian,
    "User": User,
}

while True:
    p("Library Manager:", ["Login"])
    try:
        username = r("Username: ")
        password = r("Password: ")

        # verify hashed password using helper and get user data
        x = users.verify_password(username, password)

        if x.get("status") == "disabled":
            raise Exception("This user is disabled")

        role = x.get("role")
        handler = ROLE_HANDLERS.get(role)
        if handler is None:
            raise ValueError(f"Unknown role: {role}")

        handler(x.get("name", ""), username)

    except SystemExit:
        raise
    except ConnectionFailure:
        db.e()
    except Exception as e:
        log = f"\nError: {e}"
