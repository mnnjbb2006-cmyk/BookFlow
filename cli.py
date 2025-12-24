import db
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
            choice = p(f"Welcome {name} (Admin)", ["List Users", "Add User", "Remove User", "Disable/Enable user", "Find books", "Add books", "Edit books", "Request", "Logout"])
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
                log = table(books.findbooks(r("Title: "), r("Author: "), r("Category: "), r("Min total count: "), r("Min available count: "), r("Max total count: "), r("Max available count: ")),
                ["_id", "Title", "Author", "Total count", "Available count"])
            elif choice == 6:
                log = f"\nSuccessfully addedd {books.addbook(r("Title: "), r("Author: "), r("Category: "), r("Total count: "), r("Available count: "))} books to library"
            elif choice == 7:
                pass
            elif choice == 7:
                pass
        except SystemExit:
            raise
        except Exception as e:
            log = f"\nError: {e}"

def Librarian(name, username):
    exit()

def User(name, username):
    exit()

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