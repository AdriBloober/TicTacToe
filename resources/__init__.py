import socketio

from resources.field import MatchField, EmtpyField, Field
from resources.player import CLIPlayer, WebPlayer, SocketIOClient
from threading import Thread
from flask import Flask

app = Flask(__name__)

match = None

sio = socketio.Server()
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


app_thread = None
players = []


@sio.event
def register_user(sid, data):
    global match, players, app_thread
    first = True
    if len(players) == 1:
        first = False
    if len(players) == 2:
        if not match is None:
            match = MatchField(players, 1)
            app_thread = Thread(target=match.next_turn)
            app_thread.start()
        else:
            return {"status": "error", "data": {}, "errors": ["match_started"]}

    client = SocketIOClient(sio, sid, data["name"], data["icon"], first)
    players.append(client)
    if len(players) == 2:
        match = MatchField(players, 1)
        app_thread = Thread(target=match.next_turn)
        app_thread.start()
    return {"status": "success", "errors": [], "data": client.to_json()}


app.run()

app_thread.join()
