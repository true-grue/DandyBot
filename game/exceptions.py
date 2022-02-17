class GameExceptions(Exception):
    pass


class ActionNotFoundError(GameExceptions):
    pass


class EntitiyNotFoundError(GameExceptions):
    pass


class BotNotFoundError(GameExceptions):
    pass


class LevelNotFoundError(GameExceptions):
    pass


class MapNotFoundError(GameExceptions):
    pass


class TilesConfigError(GameExceptions):
    pass
