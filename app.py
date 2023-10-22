from flask import Flask, render_template
from socketio import Server, WSGIApp

sio = Server()
app = Flask(__name__)
app.wsgi_app = WSGIApp(sio, app.wsgi_app)

messages = [{"message": "server started", "isSystem": True}]


@app.route("/")
def index():
    return render_template("index.html")


@sio.event
def connect(sid, environ, auth) -> None:
    """when client connected"""
    print("CONNECT - ", sid)
    sio.enter_room(sid, "DM")
    for msg_data in messages:
        sio.emit(
            "message",
            msg_data,
            to=sid
        )

    total = len(sio.manager.rooms["/"]["DM"])
    sio.emit(
        "message",
        {"message": f"you came into the room<br/>( total {total} )", "isSystem": True},
        to=sid,
    )
    msg_data = {
        "message": f"someone came into the room<br/>( total {total} )",
        "isSystem": True,
    }
    messages.append(msg_data)
    sio.emit(
        "message",
        msg_data,
        room="DM",
        skip_sid=sid,
    )
    sio.emit("enable_message", to=sid)


@sio.event
def disconnect(sid) -> None:
    """when client disconnected"""
    print("DISCONNECT - ", sid)
    sio.leave_room(sio, "DM")
    total = len(sio.manager.rooms["/"]["DM"]) - 1
    msg_data = {"message": f"someone left room<br/>( total {total} )", "isSystem": True}
    messages.append(msg_data)
    sio.emit(
        "message",
        msg_data,
        room="DM",
    )


@sio.event
def message(sid, data):
    """when client send message"""
    msg_data = {"message": data, "isSystem": False}
    messages.append(msg_data)
    sio.emit("message", msg_data, room="DM", skip_sid=sid)


if __name__ == "__main__":
    app.run()
