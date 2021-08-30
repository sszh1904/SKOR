from flask import Flask
from flask_cors import CORS 
from flask_socketio import SocketIO, join_room, close_room, send, emit
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'skor'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

SECTION_SOCKET_PORT = os.getenv("SECTION_SOCKET_PORT")
CERTFILE = os.getenv("CERT_FILE")
KEYFILE = os.getenv("KEY_FILE")

clientCount = 0

@app.route("/")
def messageReceived():
    print('message was received!')

@socketio.on("join")
def on_join(data):
    global clientCount
    clientCount += 1
    print("A client has successfully connected.")
    print(f"Currently there are {clientCount} clients.")
    room = data["sectionID"]
    # room = section["courseCode"] + str(section["sectionNo"])
    join_room(room)
    send(data["name"] + " has entered the room.", to=room)

@socketio.on("close")    
def on_close(data):
    room = data["sectionID"]
    emit("closeRoom", to=room)
    close_room(room)
    print(f"{room} has been closed.")

@socketio.on("refresh")
def on_refresh(data):
    room = data["sectionID"]
    email = data["email"]
    print(email + " sent a refresh to" + room + ".")
    emit("refresh", email, to=room)
    
@socketio.on("disconnect")    
def on_disconnect():
    global clientCount
    clientCount -= 1
    print("A client has disconnected.")
    print(f"Currently there are {clientCount} clients.")

if __name__ == '__main__':
    if os.getenv("LOCAL") == 'False':
        socketio.run(app, keyfile=KEYFILE, certfile=CERTFILE, host='0.0.0.0', port=SECTION_SOCKET_PORT)
    else:
        socketio.run(host='0.0.0.0', port=SECTION_SOCKET_PORT)