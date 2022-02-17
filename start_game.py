from game.exceptions import GameExceptions
from game.main import start_game


if __name__ == '__main__':
    try:
        start_game()
    except GameExceptions as ex:
        print('[GAME ERROR] ' + str(ex))
    except Exception as ex:
        print('An unhandled game error! Message: ' + str(ex))
