import sys
import time
import json
from importlib import import_module
from pathlib import Path
from random import randrange, shuffle
import tkinter as tk
from plitk import load_tileset, PliTk

SCALE = 2
DELAY = 100

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
TAKE = "take"
PASS = "pass"
PLAYER = "player"
GOLD = "gold"
WALL = "wall"
EMPTY = "empty"


class Board:
    def __init__(self, game, canvas, label):
        self.game = game
        self.canvas = canvas
        self.label = label
        self.tileset = load_tileset(game["tileset"])
        self.screen = PliTk(canvas, 0, 0, 0, 0, self.tileset, SCALE)
        self.load_players()
        self.current_round = 0
        self.load_level()

    def load_players(self):
        self.players = []
        for i, name in enumerate(self.game["players"]):
            m = import_module(name)
            tile = self.game["tiles"]["@"][i]
            self.players.append(Player(name, m.script, self, tile))
        shuffle(self.players)

    def load_level(self):
        self.steps = 0
        data = self.game["levels"][self.game["rounds"][self.current_round]]
        cols, rows = len(data[0]), len(data)
        self.canvas.config(
            width=cols * self.tileset["tile_width"] * SCALE,
            height=rows * self.tileset["tile_height"] * SCALE)
        self.screen.resize(cols, rows)
        self.level = [[data[y][x] for y in range(rows)] for x in range(cols)]
        self.has_player = [[None for y in range(rows)] for x in range(cols)]
        player_x, player_y = 0, 0
        self.cost = 0
        for y in range(rows):
            for x in range(cols):
                if self.level[x][y] == "@":
                    player_x, player_y = x, y
                    self.level[x][y] = " "
                self.cost += self.check("gold", x, y)
                self.update(x, y)
        for p in self.players:
            self.add_player(p, player_x, player_y)
        self.update_score()

    def get(self, x, y):
        if x < 0 or y < 0 or x >= self.screen.cols or y >= self.screen.rows:
            return "#"
        return self.level[x][y]

    def update(self, x, y):
        if self.has_player[x][y]:
            self.screen.set_tile(x, y, self.has_player[x][y].tile)
        else:
            self.screen.set_tile(x, y, self.game["tiles"][self.level[x][y]])

    def remove_player(self, player):
        self.has_player[player.x][player.y] = None
        self.update(player.x, player.y)

    def add_player(self, player, x, y):
        player.x, player.y = x, y
        self.has_player[x][y] = player
        self.update(x, y)

    def take_gold(self, x, y):
        self.cost -= self.check("gold", x, y)
        self.level[x][y] = " "
        self.update(x, y)
        self.update_score()

    def check(self, cmd, x, y):
        item = self.get(x, y)
        if cmd == "wall":
            return item == "#"
        if cmd == "gold":
            return int(item) if item.isdigit() else 0
        if cmd == "player":
            return item != "#" and self.has_player[x][y]

    def play(self):
        for p in self.players:
            p.act(p.script(self.check, p.x, p.y))
        self.steps += 1

    def update_score(self):
        if self.current_round < len(self.game["rounds"]):
            lines = [("Round:%4d\n" % (self.current_round + 1))]
        else:
            lines = ["Game over!\n"]
        players = sorted(self.players, key=lambda x: x.cost, reverse=True)
        for p in players:
            lines.append("%s:%4d" % (p.name, p.cost))
        self.label["text"] = "\n".join(lines)

    def next_round(self):
        self.current_round += 1
        if self.current_round < len(self.game["rounds"]):
            self.load_level()
            return True
        self.update_score()
        return False

    def is_game_ended(self):
        return self.steps >= self.game["steps"] or self.cost == 0


class Player:
    def __init__(self, name, script, board, tile):
        self.name = name
        self.script = script
        self.board = board
        self.tile = tile
        self.x, self.y = 0, 0
        self.cost = 0

    def act(self, cmd):
        dx, dy = 0, 0
        if cmd == UP:
            dy -= 1
        elif cmd == DOWN:
            dy += 1
        elif cmd == LEFT:
            dx -= 1
        elif cmd == RIGHT:
            dx += 1
        elif cmd == TAKE:
            self.take()
        self.move(dx, dy)

    def move(self, dx, dy):
        x, y = self.x + dx, self.y + dy
        board = self.board
        board.remove_player(self)
        if not board.check("wall", x, y) and not board.check("player", x, y):
            self.x, self.y = x, y
        board.add_player(self, self.x, self.y)

    def take(self):
        board = self.board
        cost = board.check("gold", self.x, self.y)
        if cost > 0:
            board.take_gold(self.x, self.y)
            self.cost += cost


def start_game():
    def update():
        t = time.time()
        board.play()
        dt = int((time.time() - t) * 1000)
        if board.is_game_ended() and not board.next_round():
            return
        root.after(max(DELAY - dt, 0), update)

    root = tk.Tk()
    root.configure(background="black")
    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(side=tk.LEFT)
    label = tk.Label(root, font=("TkFixedFont",),
                     justify=tk.RIGHT, fg="white", bg="gray20")
    label.pack(side=tk.RIGHT, anchor="n")
    game = json.loads(Path("game.json").read_text())
    board = Board(game, canvas, label)
    root.after(0, update)
    root.mainloop()


start_game()
