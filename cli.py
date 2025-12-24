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

def admin(username):
    global log
    try:
        while(True):
            choice = p(f"Welcome {username} (Admin)", ["List Users", "Add User", "Remove User", "Disable/Enable user", "Logout"])
            if choice == 5:
                return
    except SystemExit:
        raise
    except Exception as e:
        log = f"\nError: {e}"

def librarian(username):
    exit()

def user(username):
    exit()

log = ""
while(True):
    p("Library Manager:", ['Login'])
    try:
        username = r("Username: ")
        password = r("Password: ")
        x = users.getuser(username)
        if  x['password'] == password:
            eval(x['role'] + """(x["name"])""")
        else:
            ValueError("This user does not exist")
    except SystemExit:
        raise
    except Exception as e:
        log = f"\nError: {e}"