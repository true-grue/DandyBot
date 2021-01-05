import random


def script(check, x, y):
    if check("gold", x, y):
        return "take"              
    for i in range(-10, 11):
        for j in range(-10, 11):
            if check("gold", x + i, y + j):
                if not check("wall", x + 1, y) and i > 0:
                    return "right"
                if not check("wall", x - 1, y) and i < 0:
                    return "left"
                if not check("wall", x, y + 1) and j > 0:
                    return "down"
                if not check("wall", x, y - 1) and j < 0:
                    return "up"
    return random.choice(["left", "right", "up", "down"])
