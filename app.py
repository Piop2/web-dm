from flask import Flask, render_template
from socketio import Server, WSGIApp

sio = Server()
app = Flask(__name__)
app.wsgi_app = WSGIApp(sio, app.wsgi_app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
