import db
from Collections import users

def clear():
    print("\033[2J\033[H", end="")

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
            choice = p(f"Welcome {name} (Admin)", ["List Users", "Add User", "Remove User", "Disable/Enable user", "Logout"])
            if choice == 5:
                return
            elif choice == 1:
                pass
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