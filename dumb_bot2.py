import random


def script(check, x, y):
    if check("gold", x, y):
        return "take"              
    see_gold = False
    for i in range(x, x + 100):
        if check("wall", i, y):
           break
        if check("gold", i, y):
           see_gold = True
    if see_gold:
        return "right"
    for i in reversed(range(x - 100, x)):
        if check("wall", i, y):
           break
        if check("gold", i, y):
           see_gold = True
    if see_gold:
        return "left"
    for i in range(y, y + 100):
        if check("wall", x, i):
           break
        if check("gold", x, i):
           see_gold = True
    if see_gold:
        return "down"
    for i in reversed(range(y - 100, y)):
        if check("wall", x, i):
           break
        if check("gold", x, i):
           see_gold = True
    if see_gold:
        return "up"
    return random.choice(["left", "right", "up", "down"])
                
