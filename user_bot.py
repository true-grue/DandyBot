def script(check, x, y):
    if check('gold', x  , y):
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
    
        
    return "pass"
