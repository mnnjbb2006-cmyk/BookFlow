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
        x = 1
        for option in options:
            print(f"{x})", option)
            x += 1
        try:
            choice = int(r("> "))
            if choice < 0 or choice > x:
                raise
            return choice
        except:
            log = "\nYou should enter a number from the below list"

