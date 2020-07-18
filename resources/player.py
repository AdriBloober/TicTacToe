from resources.constances import NotficationType


class Player:
    def __init__(self, sio, game):
        self.sio = sio
        self.game = game

    # TODO: Notify game
    def notify_game(self, notification_type, notification_data=None):
        pass

    def force_left(self, reason):
        self.notify_game(NotficationType.FORCE_LEFT, reason)
        self.game = None
