from enum import Enum, auto

class Actions(Enum):
    TAKE = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    PASS = auto()

class Entities(Enum):
    PLAYER = auto()
    GOLD = auto()
    WALL = auto()
    EMPTY = auto()
    LEVEL = auto()
