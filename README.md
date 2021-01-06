# DandyBot

А simple programming game. You write Python scripts to control your bot in a roguelike (or [Dandy](https://en.wikipedia.org/wiki/Dandy_(video_game))-like) world. The goal is to collect as much gold as possible in the presence of other bots.

The game uses only the Python standard library. Graphics assets are from [here](https://opengameart.org/content/dungeon-crawl-32x32-tiles-supplemental).

See [random_bot.py](random_bot.py) and [user_bot.py](user_bot.py) for API examples.

## Some hints

1. You may check for "wall", "gold" and "player" at the specified position.
2. Check for the current level number, but try to generalize your code.
3. Do not use any global data or state.

![screenshot](screenshot.png)
