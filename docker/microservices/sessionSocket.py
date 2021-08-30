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

SESSION_SOCKET_PORT = os.getenv("SESSION_SOCKET_PORT")
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
    session = data["session"]
    room = session["courseCode"] + str(session["sectionNo"])
    join_room(room)
    send(data["name"] + " has entered the room.", to=room)

@socketio.on("close")    
def on_close(data):
    room = data["sectionID"]
    emit("closeRoom", to=room)
    close_room(room)
    print(f"{room} has been closed.")

@socketio.on("raiseHand")
def on_raiseHand(data):
    name = data["student"]["name"]
    sectionID = data["session"]["courseCode"] + str(data["session"]["sectionNo"])
    print(name + " from " + sectionID + " raised hand.")
    room = sectionID
    emit("addRaisehand", data, to=room, callback=messageReceived)

@socketio.on("clearHands")
def on_clearHand(data):
    print("TA cleared all hands for " + data["sectionID"] + ".")
    room = data["sectionID"]
    emit("clearHands", to=room, callback=messageReceived)
    
@socketio.on("selectHand")
def on_selectHand(data):
    print("TA selected " + data["studentEmail"] + " to answer.")
    room = data["sectionID"]
    emit("selectHand", data, to=room, callback=messageReceived)
    socketio.sleep(1)
    emit("updateChart", data["studentEmail"], to=room, callback=messageReceived)
    socketio.sleep(5)
    emit("enableRaisehand", data["studentEmail"], to=room, callback=messageReceived)
    
@socketio.on("invalid")
def on_invalid(data):
    print("TA invalidated " + data["studentEmail"] + "'s answer.")
    room = data["sectionID"]
    emit("invalid", data, to=room, callback=messageReceived)
    socketio.sleep(1)
    emit("updateChart", data["studentEmail"], to=room, callback=messageReceived)
    
@socketio.on("bonus")
def on_invalid(data):
    print("TA awarded bonus points to " + data["studentEmail"] + ".")
    room = data["sectionID"]
    emit("bonus", data, to=room, callback=messageReceived)
    socketio.sleep(1)
    emit("updateChart", data["studentEmail"], to=room, callback=messageReceived)
    
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
        socketio.run(app, keyfile=KEYFILE, certfile=CERTFILE, host='0.0.0.0', port=SESSION_SOCKET_PORT)
    else:
        socketio.run(host='0.0.0.0', port=SESSION_SOCKET_PORT)