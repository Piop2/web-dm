from flask import Flask, render_template
from socketio import Server, WSGIApp

sio = Server()
app = Flask(__name__)
app.wsgi_app = WSGIApp(sio, app.wsgi_app)

messages = []


@app.route("/")
def index():
    return render_template("index.html")


@sio.event
def connect(sid, environ, auth) -> None:
    """when client connected"""
    print("CONNECT - ", sid)
    sio.enter_room(sid, "DM")
    for msg in messages:
        sio.emit(
            "message",
            {
                "message": msg,
                "isSystem": False,
            },
            to=sid
        )

    total = len(sio.manager.rooms["/"]["DM"])
    sio.emit(
        "message",
        {"message": f"you came into the room<br/>( total {total} )", "isSystem": True},
        to=sid,
    )
    sio.emit(
        "message",
        {
            "message": f"someone came into the room<br/>( total {total} )",
            "isSystem": True,
        },
        room="DM",
        skip_sid=sid,
    )


@sio.event
def disconnect(sid) -> None:
    """when client disconnected"""
    print("DISCONNECT - ", sid)
    sio.leave_room(sio, "DM")
    total = len(sio.manager.rooms["/"]["DM"]) - 1
    sio.emit(
        "message",
        {"message": f"someone left room<br/>( total {total} )", "isSystem": True},
        room="DM",
    )


@sio.event
def message(sid, data):
    messages.append(data)
    sio.emit("message", {"message": data, "isSystem": False}, room="DM", skip_sid=sid)


if __name__ == "__main__":
    app.run(debug=True)
