from socketio import Client, Server


class Player:
    def __init__(self, name, icon, players_turn=False):
        self.name = name
        self.icon = icon
        self.players_turn = players_turn

    def get_field_location(self, match_field):
        pass

    def send_message(self, message):
        pass

    def __repr__(self):
        return self.name


class CLIPlayer(Player):
    def get_field_location(self, match_field):
        print(match_field.view_overview_without_content(True))
        return int(input("Which field would you like to place: "))

    def send_message(self, message):
        print(message)


class WebPlayer(Player):
    retrieve_field_location = False
    field_location = None

    def __init__(self, name, icon, client: Client, players_turn=False):
        self.client = client
        super().__init__(name, icon, players_turn)

    def send_message(self, message):
        self.client.emit("message", {"message": message})

    def get_field_location(self, match_field):
        self.send_message(match_field.view_overview_without_content(True))

        def callback_set_field_location(data):
            self.field_location = data["field_location"]

        self.client.emit("set_field_location", callback=callback_set_field_location)
        while self.field_location is None:
            pass
        loc = self.field_location
        self.field_location = None
        return loc

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "icon": self.icon,
            "id": self.id,
            "players_turn": self.players_turn,
        }


class SocketIOClient(Player):
    def __init__(self, sio: Server, id, name, icon, players_turn=False):
        self.sio = sio
        self.id = id
        super().__init__(name, icon, players_turn)

    def send_message(self, message):
        self.sio.emit("message", {"message": message}, room=self.id)

    def get_field_location(self, match_field):
        self.send_message(match_field.view_overview_without_content(True))
        self.field_location = None

        def callback_set_field_location(data):
            global field_location
            print(data)
            self.field_location = data

        self.sio.emit(
            "set_field_location", room=self.id, callback=callback_set_field_location
        )
        print("Wait")
        while self.field_location is None:
            pass
        print("Finished")
        return self.field_location

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "players_turn": self.players_turn
        }
