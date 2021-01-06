import random
import random_bot


def script(check, x, y):
    if check("level") == 1:
        return random_bot.script(check, x, y)
    return "pass"
