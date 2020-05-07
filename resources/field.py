from copy import deepcopy
from typing import List

from resources.player import Player, CLIPlayer


class EmtpyField:
    pass


class Field:
    def __init__(self, owned_by: Player, view: str):
        self.owned_by = owned_by
        self.view = view


def generate_black_match_field(size=3) -> List[List[Field]]:
    fields = []
    for row in range(size):
        cols = []
        for col in range(size):
            cols.append(EmtpyField)
        fields.append(cols)
    return fields


def is_all_owned_by_same(fields: List):
    if all(map(lambda field: field != EmtpyField, fields)):
        owner_of_first = fields[0].owned_by
        if all(map(lambda field: field.owned_by == owner_of_first, fields)):
            return owner_of_first
    return None


def generate_list_of_aslants(col_row_length, hor=True):
    if hor:
        l = [1]
        while len(l) < col_row_length:
            l.append(l[len(l) - 1] + col_row_length + 1)
    else:
        l = [col_row_length]
        while len(l) < col_row_length:
            l.append(l[len(l) - 1] + col_row_length - 1)
    return l


class MatchField:
    """[row, row, row]"""

    def __init__(self, players: List[Player], begining_player_index, size: int = 3):
        self.players = players
        assert len(self.players) < 3
        self.turn_player = begining_player_index
        for player in self.players:
            player.players_turn = False
        self.players[begining_player_index].players_turn = True
        self.size = size
        self.fields: List[List[Field]] = generate_black_match_field(size)

    def view(self):
        rows = []
        for raw_row in self.fields:
            row = " | "
            for raw_column in raw_row:
                if raw_column == EmtpyField:
                    row += " "
                else:
                    row += raw_column.view
                row += " | "
            rows.append(row)
        out = ""
        for row in rows:
            out += row + "\n"
        return out[: (len(out) - 2)]

    def view_overview_without_content(self, replace_not_empty_with_hashtag=False):
        rows = []
        for raw_row_index in range(len(self.fields)):
            raw_row = self.fields[raw_row_index]
            row = " | "
            for raw_column_index in range(len(raw_row)):
                raw_column = raw_row[raw_column_index]
                if replace_not_empty_with_hashtag and raw_column != EmtpyField:
                    row += "# | "
                else:
                    act = raw_column_index + 1
                    act_row = deepcopy(raw_row_index + 1)
                    while act_row > 1:
                        act += self.size
                        act_row -= 1
                    row += str(act) + " | "
            rows.append(row)
        out = ""
        for row in rows:
            out += row + "\n"
        return out[: (len(out) - 2)]

    def get_field_position_by_location(self, location: int):
        row = 1
        row_location_finder = deepcopy(location)
        while row_location_finder > self.size:
            row += 1
            row_location_finder -= self.size
        return [row - 1, row_location_finder - 1]

    def get_field_content_by_location(self, location: int):
        position = self.get_field_position_by_location(location)
        return self.fields[position[0]][position[1]]

    def set_field_content_by_location(self, location: int, content: Field):
        position = self.get_field_position_by_location(location)
        print(position)
        self.fields[position[0]][position[1]] = content

    def winning(self, player):
        for p in self.players:
            p.send_message(f"The player {player.name} ({player.icon}) wins!")
            p.send_message(self.view())
        print("Winning - ends")
        exit(0)

    def check_winning(self):
        for row in self.fields:
            p = is_all_owned_by_same(row)
            if not p is None:
                self.winning(p)
        for c in range(len(self.fields[0])):
            all = [row[c] for row in self.fields]
            p = is_all_owned_by_same(all)
            if not p is None:
                self.winning(p)
        fields = list(
            map(
                lambda location: self.get_field_content_by_location(location),
                generate_list_of_aslants(len(self.fields[0]), True),
            )
        )
        p = is_all_owned_by_same(fields)
        if not p is None:
            self.winning(p)

        fields = list(
            map(
                lambda location: self.get_field_content_by_location(location),
                generate_list_of_aslants(len(self.fields[0]), False),
            )
        )
        p = is_all_owned_by_same(fields)
        if not p is None:
            self.winning(p)

    def next_turn(self):
        self.turn_player = not self.turn_player
        for player in self.players:
            player.players_turn = False

        player = self.players[self.turn_player]
        player.players_turn = True
        print(f"Player {player} is on turn")
        cli = False
        for p in self.players:
            if not(cli and p.__class__ == CLIPlayer):
                if p.__class__ == CLIPlayer:
                    cli = True
                p.send_message(self.view() + "\n")
        while True:
            location = player.get_field_location(self)
            content = self.get_field_content_by_location(location)
            if content != EmtpyField:
                player.send_message("You must specify an not empty field.")
                continue
            self.set_field_content_by_location(location, Field(player, player.icon))
            self.check_winning()
            break
        self.next_turn()
