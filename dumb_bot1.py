import random

def script(check, x, y):
    if check("gold", x, y):
        return "take"              
    for i in range(-10, 11):
        for j in range(-10, 11):
            if check("gold", x + i, y + j):
                if not check("wall", x + 1, y) and i > 0 and i >= j:
                    return "right"
                if not check("wall", x - 1, y) and i < 0 and i <= j:
                    return "left"
                if not check("wall", x, y + 1) and j > 0 and j >= i:
                    return "down"
                if not check("wall", x, y - 1) and j < 0 and j <= i:
                    return "up"
    return random.choice(["left", "right", "up", "down"])
