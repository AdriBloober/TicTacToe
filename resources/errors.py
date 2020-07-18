class TicTacToeError(Exception):
    name = "tic_tac_toe_error"
    description = "Basic tic tac toe error."
    http_response = 500

    def __dict__(self, type="error"):
        j = {
            "name": self.name,
            "description": self.description,
            "http_response": self.http_response,
        }
        if type:
            j["type"] = type
        if self.__class__.__bases__[0] not in (TicTacToeError, Exception):
            j["parent"] = self.__class__.__bases__[0]().__dict__(type=None)
        return j


class InternalTicTacToeError(Exception):
    name = "internal_tic_tac_toe_error"
    description = "Internal tic tac toe error."
    http_response = 500

    def __dict__(self, type="error"):
        j = {
            "name": self.name,
            "description": self.description,
            "http_response": self.http_response,
        }
        if type:
            j["type"] = type
        return j


class JoiningError(TicTacToeError):
    name = "joining_error"
    description = "Basic joining error."
    http_response = 400


class GameIsRunningError(JoiningError):
    name = "game_is_running_error"
    description = "The game is is running, so you can't join it."


class MaxGameSizeReachedError(JoiningError):
    name = "max_game_size_reached_error"
    description = "The maximal game size reached, so the game is full."


class TicTacToePermissionError(TicTacToeError):
    name = "permission_error"
    description = "There's a permission error for this action."
    http_response = 403


class YouAreNotHostOfGameError(TicTacToePermissionError):
    name = "you_are_not_host_of_game_error"
    description = "You are not the host of this game, so you can't perform this action."


class GameIsRunningConfigCannotBeChangedError(TicTacToeError):
    name = "game_is_running_config_cannot_be_changed_error"
    description = "The game is running, so the config cannot be changed."
    http_response = 400


class MakeTurnError(TicTacToeError):
    name = "make_turn_error"
    description = "An error occurred during the turn."
    http_response = 400


class GameIsNotRunningError(MakeTurnError):
    name = "game_is_not_running_error"
    description = "The game is not running."


class ItsNotYourTurnError(MakeTurnError):
    name = "its_not_your_turn_error"
    description = "It's not you turn."
    http_response = 403


class FieldAlreadyOccupiedError(MakeTurnError):
    name = "field_already_occupied"
    description = "The field is already occupied."


class InvalidFieldLocationError(MakeTurnError):
    name = "invalid_field_location_error"
    description = "The field location is invalid."


class PlayerNotFoundError(TicTacToeError):
    name = "player_not_found_error"
    description = "The player was not found."
    http_response = 404


class BadRequestError(TicTacToeError):
    name = "bad_request_error"
    description = "The request arguments are invalid."
    http_response = 400
