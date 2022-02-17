from game.api import Actions, Entities
import random


def script(check, x, y):
    if check(Entities.EMPTY, x, y):
        return Actions.TAKE
    return random.choice([Actions.PASS, Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN])
