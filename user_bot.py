def script(check, x, y):
    if check('gold', x, y):
        return "take"
    if check('gold', x + 1, y):
        return "right"
    if check('gold', x - 1, y):
        return "left"
    if check('gold', x, y + 1):
        return "down"
    if check('gold', x, y - 1):
        return "up"

    elif check("level") == 1:
        return "right"

    elif check("level") == 2:
        if check("gold", x + 2, y):
            return "right"
        return "up"

    elif check("level") == 3:
        if (check("wall", x, y - 1) != 1 and check("wall", x - 1, y + 1) and check("wall", x - 1, y) != 1) or (check("wall", x, y + 1) and check("wall", x - 1, y) != 1):
            return "left"
        elif (check("wall", x, y - 1) or check("wall", x + 1, y - 1)) and check("wall", x + 1, y) != 1:
            return "right"
        elif check("wall", x + 1, y - 1) or (check("wall", x + 1, y + 1) and check("wall", x - 1, y) != 1):
            return "down"
        elif (check("wall", x, y - 1) != 1 and check("wall", x - 1, y - 1)) or check("wall", x, y - 1) != 1 and check("wall", x - 1, y):
            return "up"
        return "pass"

    elif check("level") == 4:
        if check("gold", x-4, y) and check("wall", x-1, y) != 1 and check("wall", x+1, y+1):
            return "left"
        if check("wall", x+2, y) and check("wall", x-1, y) != 1 and check("wall", x-1, y-1) and check("wall", x-1, y+3):
            return "right"
        if check("gold", x+3, y) != 1 and check("gold", x+4, y) and check("wall", x, y-1) != 1:
            print(1)
            return "right"
        if (check("wall", x, y - 1) != 1 and check("wall", x - 1, y + 1) and check("wall", x - 1, y) != 1) or (check("wall", x, y + 1) and check("wall", x - 1, y) != 1):
            return "left"
        elif (check("wall", x, y - 1) or check("wall", x + 1, y - 1)) and check("wall", x + 1, y) != 1:
            return "right"
        elif check("wall", x + 1, y - 1) or (check("wall", x + 1, y + 1) and check("wall", x - 1, y) != 1):
            return "down"
        elif (check("wall", x, y - 1) != 1 and check("wall", x - 1, y - 1)) or check("wall", x, y - 1) != 1 and check("wall", x - 1, y):
            return "up"

        return "pass"
