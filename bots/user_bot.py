from game.api import Actions, Entities


def script(check, x, y):
    if check(Entities.LEVEL) == 1:
        return Actions.RIGHT
    return Actions.PASS
