from enum import Enum


class GameStatus(Enum):
    WAITING_FOR_PLAYERS = 0
    WAITING_FOR_STARTING = 1
    RUNNING = 2


class NotficationType(Enum):
    STATUS_CHANGE = 0
    PLAYER_JOINED = 1
    PLAYER_LEFT = 2
    GAME_FINISHED = 3
    FORCE_LEFT = 4
    CONFIG_CHANGED = 5
    GAME_WAS_STARTED = 6
    TURN_WAS_MADE = 7


class ForceLeftReason(Enum):
    HOST_LEFT_GAME = 0
    TIMEOUT = 1
    KICKED = 2
