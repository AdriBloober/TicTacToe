from typing import List, Set, Tuple

from resources.constances import GameStatus, NotficationType, ForceLeftReason
from resources.errors import (
    GameIsRunningError,
    MaxGameSizeReachedError,
    YouAreNotHostOfGameError,
    GameIsRunningConfigCannotBeChangedError,
    GameIsNotRunningError,
    ItsNotYourTurnError,
    FieldAlreadyOccupiedError,
    InvalidFieldLocationError,
    PlayerNotFoundError,
)


class Game(object):
    """Game object
    field: List[List[Integer]].
    field Integer:
        -1 : The field is empty.
        Any other integer: The index integer for players list.
    players: List[Player]
    player_on_turn:
        -1 : Nobody is on turn (game was not started).
        Any other integer: The index integer for players list.
    """

    field: List[List[int]]
    player_max_size = 2
    player_min_size = 2

    @property
    def player_size(self):
        return len(self.players)

    def generate_field(self):
        self.field = [
            [-1 for _ in range(self.field_size)] for _ in range(self.field_size)
        ]

    def __init__(self, group_name, private: bool, players: list, field_size: int = 3):
        self.group_name = group_name
        self.private = private
        self.players = players
        self.field_size = field_size
        self.generate_field()
        self.status = GameStatus.WAITING_FOR_PLAYERS
        self.player_on_turn = -1

    def change_status(self, status):
        self.status = status
        [
            player.notify_game(NotficationType.STATUS_CHANGE, status)
            for player in self.players
        ]

    def join_player(self, player):
        if self.status == GameStatus.RUNNING:
            raise GameIsRunningError()
        if self.player_size >= self.player_max_size:
            raise MaxGameSizeReachedError()
        self.players.append(player)
        [
            player.notify_game(NotficationType.PLAYER_JOINED, player)
            for player in self.players
        ]
        if self.player_size >= self.player_min_size:
            self.change_status(GameStatus.WAITING_FOR_STARTING)

    def check_player_on_turn(self, player):
        if self.players.index(player) != self.player_on_turn:
            raise ItsNotYourTurnError()

    def check_host(self, player):
        if self.players.index(player) != 0:
            raise YouAreNotHostOfGameError()

    def finish_game(self, data=None):
        self.__init__(self.group_name, self.players, field_size=self.field_size)
        [
            player.notify_game(NotficationType.GAME_FINISHED, data)
            for player in self.players
        ]

    def left_player(self, player):
        if self.players.index(player) == 0:
            self.players.remove(player)
            [
                player.force_left(ForceLeftReason.HOST_LEFT_GAME)
                for player in self.players
            ]
        else:
            self.players.remove(player)
        self.finish_game()

    def change_field_size(self, player, new_field_size: int):
        self.check_host(player)
        if self.status == GameStatus.RUNNING:
            raise GameIsRunningConfigCannotBeChangedError()
        self.field_size = new_field_size
        self.generate_field()
        [player.notify_game(NotficationType.CONFIG_CHANGED) for player in self.players]

    def start_game(self, player):
        self.check_host(player)
        self.player_on_turn = 0
        self.status = GameStatus.RUNNING
        [
            player.notify_game(NotficationType.GAME_WAS_STARTED)
            for player in self.players
        ]

    def rotate_player_turn(self):
        self.player_on_turn = int(not self.player_on_turn)

    def winning(self, p):
        self.finish_game(p)

    def if_same_winning(self, l):
        a = True
        b = []
        for i in l:
            if len(b) == 0 and i != -1:
                b.append(i)
            else:
                if i not in b or i == -1:
                    a = False
                    break
        return a, b[0]

    def check_winning(self):
        for i in self.field:
            winning, player = self.if_same_winning(i)
            if winning:
                return self.winning(self.players[player])
        for i in range(len(self.field[0])):
            l = []
            for b in self.field:
                l.append(b[i])
            winning, player = self.if_same_winning(l)
            if winning:
                return self.winning(self.players[player])
        if self.field_size % 2 != 0:
            l1 = []
            l2 = []
            for i in range(self.field_size - 1):
                l1.append(self.field[i][i])
                l2.append(self.field[i][self.field_size - 1 - i])
            winning1, player1 = self.if_same_winning(l1)
            winning2, player2 = self.if_same_winning(l2)
            if winning1:
                return self.winning(self.players[player1])
            if winning2:
                return self.winning(self.players[player2])

    def do_turn(self, player, field_location: Tuple[int, int]):
        if self.status != GameStatus.RUNNING:
            raise GameIsNotRunningError()
        self.check_player_on_turn(player)
        try:
            value = self.field[field_location[0]][field_location[1]]
            if value != -1:
                raise FieldAlreadyOccupiedError()
            self.field[field_location[0]][field_location[1]] = self.players.index(
                player
            )
            self.rotate_player_turn()
            [
                player.notify_game(NotficationType.TURN_WAS_MADE)
                for player in self.players
            ]
        except KeyError:
            raise InvalidFieldLocationError()
        self.check_winning()

    def kick_player(self, player, target_player_id):
        self.check_host(player)
        if target_player_id > self.player_size + 1 or target_player_id < 0:
            raise PlayerNotFoundError()
        else:
            target_player = self.players[target_player_id]
            self.players.remove(target_player)
            self.left_player(target_player)
            target_player.notify_game(NotficationType.FORCE_LEFT, ForceLeftReason.KICKED)
