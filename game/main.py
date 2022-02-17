import time
import sys
import json
import tkinter as tk
import importlib.resources
from importlib import import_module
from random import shuffle
from game.exceptions import ActionNotFoundError, BotNotFoundError, EntitiyNotFoundError, LevelNotFoundError, MapNotFoundError, TilesConfigError
from game.plitk import load_tileset, PliTk
from game.api import Entities, Actions

SCALE = 1
DELAY = 50


class Board:
    def __init__(self, game, canvas, label):
        self.game = game
        self.canvas = canvas
        self.label = label
        self.tileset = load_tileset(game["tileset"])
        self.screen = PliTk(canvas, 0, 0, 0, 0, self.tileset, SCALE)
        self.load_players()
        self.level_index = 0
        self.load_level()

    def load_players(self):
        self.players = []
        for i, name in enumerate(self.game["players"]):
            try:
                script = import_module('bots.' + name).script
                tile = self.game["tiles"]["@"][i]
                self.players.append(Player(name, script, self, tile))
            except ModuleNotFoundError:
                raise BotNotFoundError(
                    "Bot with name '{}' not found".format(name))
            except KeyError:
                raise TilesConfigError(
                    "Tiles config are empty or set incorrectly")
        shuffle(self.players)

    def load_level(self):
        self.gold = 0
        self.steps = 0

        try:
            self.level = self.game["levels"][self.level_index]
        except IndexError:
            raise LevelNotFoundError(
                "Level with index {} not found".format(self.level_index))

        try:
            data = self.game["maps"][self.level["map"]]
        except IndexError:
            raise MapNotFoundError(
                "Map with index {} not found".format(self.level["map"]))

        cols, rows = len(data[0]), len(data)
        self.map = [[data[y][x] for y in range(rows)] for x in range(cols)]
        self.has_player = [[None for y in range(rows)] for x in range(cols)]
        self.canvas.config(width=cols * self.tileset["tile_width"] * SCALE,
                           height=rows * self.tileset["tile_height"] * SCALE)
        self.screen.resize(cols, rows)
        for y in range(rows):
            for x in range(cols):
                self.update(x, y)
        for p in self.players:
            self.add_player(p, *self.level["start"])
        self.update_score()

    def get(self, x, y):
        if x < 0 or y < 0 or x >= self.screen.cols or y >= self.screen.rows:
            return "#"
        return self.map[x][y]

    def update(self, x, y):
        if self.has_player[x][y]:
            self.screen.set_tile(x, y, self.has_player[x][y].tile)
        else:
            self.screen.set_tile(x, y, self.game["tiles"][self.map[x][y]])

    def remove_player(self, player):
        self.has_player[player.x][player.y] = None
        self.update(player.x, player.y)

    def add_player(self, player, x, y):
        player.x, player.y = x, y
        self.has_player[x][y] = player
        self.update(x, y)

    def take_gold(self, x, y):
        self.gold += self.check(Entities.GOLD, x, y)
        self.map[x][y] = " "
        self.update(x, y)
        self.update_score()

    def check(self, cmd, *args):
        if cmd == Entities.LEVEL:
            return self.level_index + 1
        x, y = args
        item = self.get(x, y)
        if cmd == Entities.WALL:
            return item == "#"
        elif cmd == Entities.GOLD:
            return int(item) if item.isdigit() else 0
        elif cmd == Entities.PLAYER:
            return item != "#" and self.has_player[x][y]
        elif cmd != Entities.EMPTY:
            raise EntitiyNotFoundError(
                "The entity '{}' does not exist".format(cmd))

    def play(self):
        for p in self.players:
            p.act(p.script(self.check, p.x, p.y))
            if self.gold >= self.level["gold"]:
                return self.select_next_level()
        self.steps += 1
        return self.steps < self.level["steps"]

    def update_score(self):
        lines = [("Level:%4d\n" % (self.level_index + 1))]
        players = sorted(self.players, key=lambda x: x.gold, reverse=True)
        for p in players:
            lines.append("%s:%4d" % (p.name, p.gold))
        self.label["text"] = "\n".join(lines)

    def select_next_level(self):
        self.level_index += 1
        if self.level_index < len(self.game["levels"]):
            self.load_level()
            return True
        return False


class Player:
    def __init__(self, name, script, board, tile):
        self.name = name
        self.script = script
        self.board = board
        self.tile = tile
        self.x, self.y = 0, 0
        self.gold = 0

    def act(self, cmd):
        dx, dy = 0, 0
        if cmd == Actions.UP:
            dy -= 1
        elif cmd == Actions.DOWN:
            dy += 1
        elif cmd == Actions.LEFT:
            dx -= 1
        elif cmd == Actions.RIGHT:
            dx += 1
        elif cmd == Actions.TAKE:
            self.take()
        elif cmd != Actions.PASS:
            raise ActionNotFoundError(
                "The action '{}' does not exist".format(cmd))
        self.move(dx, dy)

    def move(self, dx, dy):
        x, y = self.x + dx, self.y + dy
        board = self.board
        board.remove_player(self)
        if not board.check(Entities.WALL, x, y) and not board.check(Entities.PLAYER, x, y):
            self.x, self.y = x, y
        board.add_player(self, self.x, self.y)

    def take(self):
        gold = self.board.check(Entities.GOLD, self.x, self.y)
        if gold:
            self.gold += gold
            self.board.take_gold(self.x, self.y)


def start_game():
    def update():
        t = time.time()
        if board.play():
            dt = int((time.time() - t) * 1000)
            root.after(max(DELAY - dt, 0), update)
        else:
            label["text"] += "\n\nGAME OVER!"

    root = tk.Tk()
    root.configure(background="black")
    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(side=tk.LEFT)
    label = tk.Label(root, font=("TkFixedFont",),
                     justify=tk.RIGHT, fg="white", bg="gray20")
    label.pack(side=tk.RIGHT, anchor="n")
    filename = sys.argv[1] if len(sys.argv) == 2 else "game.json"
    game = json.loads(importlib.resources.read_text('game', filename))
    board = Board(game, canvas, label)
    root.after(0, update)
    root.mainloop()
