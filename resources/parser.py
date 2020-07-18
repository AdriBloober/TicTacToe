import json

from resources.errors import InternalTicTacToeError, BadRequestError


class ParserArgumentAlreadyExists(InternalTicTacToeError):
    def __init__(self, argument):
        self.parser_argument = argument
        super().__init__(f"The parser argument {argument} already exists.")


class ParserArgument:
    def __init__(self, type=str, default=None, required=False):
        self.type = type
        self.default = type(default)
        self.required = required

    def parse_arg(self, j, error=BadRequestError):
        if j in (None, "", {}):
            if self.default is not None:
                return self.default
            elif self.required:
                raise error()
            else:
                return None
        try:
            return self.type(j)
        except ValueError:
            raise error()


class Parser:
    arguments = {}

    def add_argument(self, name, type=str, default=None, required=False):
        if name in self.arguments:
            raise ParserArgumentAlreadyExists(name)
        self.arguments[name] = ParserArgument(
            type=type, default=default, required=required
        )

    def parse_arguments(self, j, error=BadRequestError):
        if type(j) != dict:
            j = json.loads(j)
        j_out = {}
        for arg_name, arg in self.arguments.items():
            j_out[arg_name] = arg.parse_arg(j.get(arg_name, None), error=error)
        return j_out
